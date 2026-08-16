import json
from typing import Any, Dict
from app.ai.clients.gemini import GeminiClient
from app.ai.prompts.email_prompt import EMAIL_GENERATOR_PROMPT

class EmailGenerator:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    async def generate_email(
        self,
        template_type: str,
        candidate_name: str,
        job_title: str,
        recruiter_name: str,
        additional_context: str = ""
    ) -> Dict[str, str]:
        """Generate personalized emails from recruiters to candidates."""
        prompt = EMAIL_GENERATOR_PROMPT.format(
            template_type=template_type,
            candidate_name=candidate_name,
            job_title=job_title,
            recruiter_name=recruiter_name,
            additional_context=additional_context
        )
        response_text = await self.gemini_client.call_llm(prompt)
        clean_json = self._clean_json(response_text)
        
        parsed_data = {}
        try:
            parsed_data = json.loads(clean_json)
        except Exception:
            pass

        subject = (
            parsed_data.get("subject")
            or parsed_data.get("email_subject")
            or parsed_data.get("title")
            or f"Update regarding your application for {job_title}"
        )

        body = (
            parsed_data.get("body")
            or parsed_data.get("email_body")
            or parsed_data.get("content")
            or parsed_data.get("message")
            or parsed_data.get("text")
            or parsed_data.get("body_text")
        )

        if not body or not isinstance(body, str) or not body.strip():
            body = self._get_fallback_body(template_type, candidate_name, job_title, recruiter_name)

        return {
            "subject": subject.strip(),
            "body": body.strip(),
        }

    def _get_fallback_body(self, template_type: str, candidate_name: str, job_title: str, recruiter_name: str) -> str:
        tt = (template_type or "").lower()
        if "interview" in tt or "invitation" in tt:
            return (
                f"Dear {candidate_name},\n\n"
                f"Thank you for applying for the {job_title} role at HireMind. We were very impressed with your background and experience!\n\n"
                f"We would love to invite you for an initial interview to discuss your qualifications further. Please let us know your availability over the coming days.\n\n"
                f"Best regards,\n{recruiter_name}"
            )
        elif "shortlist" in tt:
            return (
                f"Dear {candidate_name},\n\n"
                f"We are pleased to inform you that your application for the {job_title} position has been shortlisted for the next round!\n\n"
                f"Our team will be in touch shortly with details regarding the technical assessment.\n\n"
                f"Best regards,\n{recruiter_name}"
            )
        elif "rejection" in tt:
            return (
                f"Dear {candidate_name},\n\n"
                f"Thank you for your interest in the {job_title} position and for taking the time to share your background with us.\n\n"
                f"After careful review of all applications, we have decided to move forward with other candidates whose experience more closely matches our current requirements.\n\n"
                f"We appreciate your interest in our company and wish you all the best in your job search.\n\n"
                f"Best regards,\n{recruiter_name}"
            )
        elif "offer" in tt:
            return (
                f"Dear {candidate_name},\n\n"
                f"We are thrilled to offer you the position of {job_title} at HireMind!\n\n"
                f"We were incredibly impressed by your skills and experience during the interview process and believe you will be a fantastic addition to our team.\n\n"
                f"Best regards,\n{recruiter_name}"
            )
        else:
            return (
                f"Dear {candidate_name},\n\n"
                f"I hope this message finds you well. I wanted to follow up regarding your application for the {job_title} position.\n\n"
                f"Please let us know if you have any questions or updates regarding your application status.\n\n"
                f"Best regards,\n{recruiter_name}"
            )

    def _clean_json(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text.strip()
