from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.ai.clients.gemini import GeminiClient
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.parser.resume_parser import ResumeParser
from app.ai.matcher.resume_matcher import ResumeMatcher
from app.ai.ranking.candidate_ranker import CandidateRanker
from app.ai.summary.summary_generator import SummaryGenerator
from app.ai.questions.question_generator import QuestionGenerator
from app.ai.emails.email_generator import EmailGenerator
from app.ai.chat.recruiter_chat import RecruiterChat
from app.schemas.ai import (
    ParseRequest,
    MatchRequest,
    RankRequest,
    SummaryRequest,
    QuestionsRequest,
    ChatRequest,
    EmailRequest,
)

router = APIRouter(prefix="/ai", tags=["AI Processing Engine"])

# Unified instances provider dependency injects
def get_gemini_client() -> GeminiClient:
    return GeminiClient()

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

def get_parser(client: GeminiClient = Depends(get_gemini_client)) -> ResumeParser:
    return ResumeParser(client)

def get_matcher(client: GeminiClient = Depends(get_gemini_client)) -> ResumeMatcher:
    return ResumeMatcher(client)

def get_ranker(client: GeminiClient = Depends(get_gemini_client)) -> CandidateRanker:
    return CandidateRanker(client)

def get_summary_gen(client: GeminiClient = Depends(get_gemini_client)) -> SummaryGenerator:
    return SummaryGenerator(client)

def get_question_gen(client: GeminiClient = Depends(get_gemini_client)) -> QuestionGenerator:
    return QuestionGenerator(client)

def get_email_gen(client: GeminiClient = Depends(get_gemini_client)) -> EmailGenerator:
    return EmailGenerator(client)

def get_chat_assistant(
    client: GeminiClient = Depends(get_gemini_client),
    embed: EmbeddingService = Depends(get_embedding_service)
) -> RecruiterChat:
    return RecruiterChat(client, embed)


@router.post("/parse", status_code=status.HTTP_200_OK)
async def parse_resume_content(
    payload: ParseRequest,
    current_user: User = Depends(get_current_user),
    parser_service: ResumeParser = Depends(get_parser)
) -> Dict[str, Any]:
    """Parse candidate resume raw text content into structural JSON."""
    return await parser_service.parse(payload.raw_text)


@router.post("/match", status_code=status.HTTP_200_OK)
async def match_resume_to_job(
    payload: MatchRequest,
    current_user: User = Depends(get_current_user),
    matcher_service: ResumeMatcher = Depends(get_matcher)
) -> Dict[str, Any]:
    """Evaluate candidate resume profile fit against a target job description."""
    return await matcher_service.match(
        resume_text=payload.resume_text,
        job_title=payload.job_title,
        job_description=payload.job_description,
        job_requirements=payload.job_requirements
    )


@router.post("/rank", status_code=status.HTTP_200_OK)
async def rank_candidates_fit(
    payload: RankRequest,
    current_user: User = Depends(get_current_user),
    ranker_service: CandidateRanker = Depends(get_ranker)
) -> Dict[str, Any]:
    """Rank list of candidate summaries against a target job description."""
    return await ranker_service.rank_candidates(payload.job_description, payload.candidates)


@router.post("/summary", status_code=status.HTTP_200_OK)
async def generate_resume_summary(
    payload: SummaryRequest,
    current_user: User = Depends(get_current_user),
    summary_service: SummaryGenerator = Depends(get_summary_gen)
) -> str:
    """Generate concise recruiter-friendly resume profile summaries."""
    return await summary_service.generate_summary(payload.resume_text)


@router.post("/questions", status_code=status.HTTP_200_OK)
async def generate_interview_questions(
    payload: QuestionsRequest,
    current_user: User = Depends(get_current_user),
    questions_service: QuestionGenerator = Depends(get_question_gen)
) -> Dict[str, Any]:
    """Generate customized interview prep questionnaires based on gaps analysis."""
    return await questions_service.generate_questions(
        job_description=payload.job_description,
        resume_text=payload.resume_text,
        skill_gaps=payload.skill_gaps
    )


@router.post("/chat", status_code=status.HTTP_200_OK)
async def query_recruiter_assistant(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    chat_service: RecruiterChat = Depends(get_chat_assistant)
) -> str:
    """Query the recruiter assistant copilot using natural language RAG searches."""
    org_id = current_user.organization_id or "default-org-id"
    return await chat_service.answer_query(payload.query, org_id)


@router.post("/email", status_code=status.HTTP_200_OK)
async def generate_recruiter_email(
    payload: EmailRequest,
    current_user: User = Depends(get_current_user),
    email_service: EmailGenerator = Depends(get_email_gen)
) -> Dict[str, str]:
    """Generate personalized candidate email communications template."""
    return await email_service.generate_email(
        template_type=payload.template_type,
        candidate_name=payload.candidate_name,
        job_title=payload.job_title,
        recruiter_name=payload.recruiter_name,
        additional_context=payload.additional_context
    )
