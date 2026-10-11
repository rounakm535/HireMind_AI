import uuid
import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from app.schemas.resume import EmailLogResponse
from app.dependencies.auth import get_resume_service, RoleChecker
from app.services.resume_service import ResumeService
from app.models.user import User, UserRole
from app.exceptions.custom import PermissionDeniedError
from app.models.match import EmailLog
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/emails", tags=["Emails"])

write_checker = RoleChecker([UserRole.ADMIN, UserRole.RECRUITER])


class EmailGenerateRequest(BaseModel):
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    template_type: str  # interview_invitation, shortlist, rejection, etc.


class EmailSendRequest(BaseModel):
    candidate_id: Optional[uuid.UUID] = None
    recipient_email: str
    subject: str
    body: str


def dispatch_smtp(recipient_email: str, subject: str, body: str) -> tuple[bool, Optional[str]]:
    """Helper function to dispatch email over SMTP if credentials are valid, trying both 465 and 587."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        return False, "SMTP user or app password not configured."

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    message["To"] = recipient_email
    message.attach(MIMEText(body, "plain"))

    errors = []
    ports = [465, 587] if settings.SMTP_PORT == 465 else [settings.SMTP_PORT, 465]
    ports = list(dict.fromkeys(ports))

    context = ssl.create_default_context()
    for port in ports:
        try:
            if port == 465:
                with smtplib.SMTP_SSL(settings.SMTP_HOST, port, context=context, timeout=8) as server:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.sendmail(settings.SMTP_FROM_EMAIL, recipient_email, message.as_string())
            else:
                with smtplib.SMTP(settings.SMTP_HOST, port, timeout=8) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.sendmail(settings.SMTP_FROM_EMAIL, recipient_email, message.as_string())
            logger.info(f"Successfully dispatched real SMTP email to {recipient_email} via port {port}")
            return True, None
        except Exception as e:
            err_msg = f"Port {port}: {type(e).__name__} ({str(e)})"
            logger.warning(f"SMTP delivery warning for {recipient_email}: {err_msg}")
            errors.append(err_msg)

def dispatch_https_api(recipient_email: str, subject: str, body: str) -> tuple[bool, Optional[str]]:
    """Send via Brevo or Resend over HTTPS port 443 (never blocked by cloud firewalls)."""
    import urllib.request
    import json

    if settings.BREVO_API_KEY:
        try:
            req = urllib.request.Request(
                "https://api.brevo.com/v3/smtp/email",
                data=json.dumps({
                    "sender": {"name": settings.SMTP_FROM_NAME, "email": settings.SMTP_FROM_EMAIL},
                    "to": [{"email": recipient_email}],
                    "subject": subject,
                    "textContent": body,
                }).encode(),
                headers={
                    "api-key": settings.BREVO_API_KEY,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status in (200, 201):
                    logger.info(f"Dispatched email to {recipient_email} via Brevo HTTPS API")
                    return True, None
        except Exception as e:
            err_msg = f"Brevo API: {e}"
            logger.warning(f"Brevo error for {recipient_email}: {err_msg}")
            return False, err_msg

    if settings.RESEND_API_KEY:
        try:
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=json.dumps({
                    "from": f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>",
                    "to": [recipient_email],
                    "subject": subject,
                    "text": body,
                }).encode(),
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status in (200, 201):
                    logger.info(f"Dispatched email to {recipient_email} via Resend HTTPS API")
                    return True, None
        except Exception as e:
            err_msg = f"Resend API: {e}"
            logger.warning(f"Resend error for {recipient_email}: {err_msg}")
            return False, err_msg

    return False, "No HTTPS email provider configured."


def dispatch_email(recipient_email: str, subject: str, body: str) -> tuple[bool, Optional[str]]:
    """Dispatch email using HTTPS API if available, falling back to direct SMTP."""
    if settings.BREVO_API_KEY or settings.RESEND_API_KEY:
        success, err = dispatch_https_api(recipient_email, subject, body)
        if success:
            return True, None

    return dispatch_smtp(recipient_email, subject, body)


@router.post("/generate", response_model=EmailLogResponse, status_code=status.HTTP_201_CREATED)
async def generate_email(
    request: EmailGenerateRequest,
    current_user: User = Depends(write_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")
    return await resume_service.generate_candidate_email(
        candidate_id=request.candidate_id,
        job_id=request.job_id,
        template_type=request.template_type,
        sender_id=current_user.id,
        organization_id=current_user.organization_id,
    )


@router.post("/send", response_model=EmailLogResponse, status_code=status.HTTP_201_CREATED)
async def send_direct_email(
    request: EmailSendRequest,
    current_user: User = Depends(write_checker),
    resume_service: ResumeService = Depends(get_resume_service),
):
    if not current_user.organization_id:
        raise PermissionDeniedError("User must belong to an organization.")

    import asyncio
    loop = asyncio.get_running_loop()
    # Attempt real email transmission (HTTPS API or SMTP)
    success, error_detail = await loop.run_in_executor(
        None, lambda: dispatch_email(request.recipient_email, request.subject, request.body)
    )

    status_str = "SENT" if success else "FAILED"
    email_log = EmailLog(
        sender_id=current_user.id,
        recipient_email=request.recipient_email,
        subject=request.subject,
        body=request.body,
        status=status_str,
    )
    saved_log = await resume_service.resume_repo.create_email_log(email_log)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Email dispatch failed ({error_detail}). Cloud hosting providers like Render often block outbound SMTP. Please use 'Send via Gmail' or 'Open in Mail App' to dispatch directly."
        )

    return saved_log
