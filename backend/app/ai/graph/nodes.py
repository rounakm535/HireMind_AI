import logging
from typing import Any, Dict, List
from app.ai.clients.gemini import GeminiClient
from app.ai.embeddings.embedding_service import EmbeddingService
from app.ai.parser.resume_parser import ResumeParser
from app.ai.matcher.resume_matcher import ResumeMatcher
from app.ai.ranking.candidate_ranker import CandidateRanker
from app.ai.summary.summary_generator import SummaryGenerator
from app.ai.questions.question_generator import QuestionGenerator
from app.ai.graph.state import ScreenResumeState

logger = logging.getLogger(__name__)

# Initialize dependencies
gemini_client = GeminiClient()
embedding_service = EmbeddingService()

parser = ResumeParser(gemini_client)
matcher = ResumeMatcher(gemini_client)
ranker = CandidateRanker(gemini_client)
summarizer = SummaryGenerator(gemini_client)
question_gen = QuestionGenerator(gemini_client)


async def parse_resume_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Parse candidate resume text using Gemini."""
    logger.info("Executing parse_resume_node...")
    try:
        raw_text = state.get("resume_raw_text", "")
        parsed = await parser.parse(raw_text)
        return {"parsed_resume": parsed}
    except Exception as e:
        logger.error(f"Error in parse_resume_node: {e}")
        return {"errors": [f"Parsing error: {str(e)}"]}


async def generate_embeddings_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Generate vector embeddings for the candidate resume."""
    logger.info("Executing generate_embeddings_node...")
    try:
        raw_text = state.get("resume_raw_text", "")
        vector = await embedding_service.get_embedding(raw_text)
        return {"embeddings": vector}
    except Exception as e:
        logger.error(f"Error in generate_embeddings_node: {e}")
        return {"errors": [f"Embeddings error: {str(e)}"]}


async def store_vector_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Store resume embeddings and metadata in Qdrant."""
    logger.info("Executing store_vector_node...")
    try:
        resume_id = state.get("resume_id") or "temp-resume-id"
        raw_text = state.get("resume_raw_text", "")
        parsed = state.get("parsed_resume") or {}
        candidate_info = parsed.get("candidate_info", {})
        
        metadata = {
            "resume_id": resume_id,
            "candidate_id": state.get("candidate_id"),
            "organization_id": state.get("organization_id"),
            "first_name": candidate_info.get("first_name", ""),
            "last_name": candidate_info.get("last_name", ""),
            "email": candidate_info.get("email", ""),
            "skills": parsed.get("skills", [])
        }
        await embedding_service.store_resume_vector(resume_id, raw_text, metadata)
        return {}
    except Exception as e:
        logger.error(f"Error in store_vector_node: {e}")
        return {"errors": [f"Vector store error: {str(e)}"]}


async def retrieve_candidates_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Retrieve semantically similar candidates from Qdrant vector store."""
    logger.info("Executing retrieve_candidates_node...")
    try:
        job_desc = state.get("job_description", "")
        results = await embedding_service.search_candidates(job_desc, limit=5)
        
        candidates_list = []
        for r in results:
            meta = r.get("metadata", {})
            candidates_list.append({
                "id": meta.get("candidate_id"),
                "name": f"{meta.get('first_name')} {meta.get('last_name')}",
                "score": r.get("score"),
                "summary": meta.get("skills", [])
            })
        return {"similar_candidates": candidates_list}
    except Exception as e:
        logger.error(f"Error in retrieve_candidates_node: {e}")
        return {"errors": [f"Retrieve candidates error: {str(e)}"]}


async def resume_matching_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Perform resume matching against target job description requirements."""
    logger.info("Executing resume_matching_node...")
    try:
        raw_text = state.get("resume_raw_text", "")
        title = state.get("job_title", "")
        desc = state.get("job_description", "")
        reqs = state.get("job_requirements", "")
        
        match_data = await matcher.match(
            resume_text=raw_text,
            job_title=title,
            job_description=desc,
            job_requirements=reqs
        )
        return {
            "match_score": match_data.get("score", 50.0),
            "fit_explanation": match_data.get("fit_explanation", ""),
            "matching_skills": match_data.get("matching_skills", []),
            "missing_skills": match_data.get("missing_skills", []),
            "experience_match": match_data.get("experience_match", ""),
            "education_match": match_data.get("education_match", ""),
            "hiring_recommendation": match_data.get("hiring_recommendation", "")
        }
    except Exception as e:
        logger.error(f"Error in resume_matching_node: {e}")
        return {"errors": [f"Resume matching error: {str(e)}"]}


async def skill_gap_analysis_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Perform detailed skill gap analysis against job requirements."""
    logger.info("Executing skill_gap_analysis_node...")
    try:
        raw_text = state.get("resume_raw_text", "")
        reqs = state.get("job_requirements", "")
        
        gap_data = await matcher.analyze_skill_gap(
            candidate_skills=raw_text,
            job_requirements=reqs
        )
        return {"skill_gap": gap_data}
    except Exception as e:
        logger.error(f"Error in skill_gap_analysis_node: {e}")
        return {"errors": [f"Skill gap analysis error: {str(e)}"]}


async def ranking_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Rank retrieved candidates using Gemini context reasoning."""
    logger.info("Executing ranking_node...")
    try:
        desc = state.get("job_description", "")
        candidates = state.get("similar_candidates") or []
        
        # Inject the current candidate if not already present
        curr_id = state.get("candidate_id") or "current-candidate"
        curr_parsed = state.get("parsed_resume") or {}
        curr_meta = curr_parsed.get("candidate_info", {})
        
        has_current = any(c.get("id") == curr_id for c in candidates)
        if not has_current:
            candidates.append({
                "id": curr_id,
                "name": f"{curr_meta.get('first_name', 'Current')} {curr_meta.get('last_name', 'Candidate')}",
                "score": state.get("match_score", 50.0),
                "summary": state.get("summary", "")
            })
            
        rankings = await ranker.rank_candidates(desc, candidates)
        return {"rankings": rankings.get("rankings", [])}
    except Exception as e:
        logger.error(f"Error in ranking_node: {e}")
        return {"errors": [f"Ranking error: {str(e)}"]}


async def summary_generation_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Generate concise recruiter-friendly resume summaries."""
    logger.info("Executing summary_generation_node...")
    try:
        raw_text = state.get("resume_raw_text", "")
        summary_text = await summarizer.generate_summary(raw_text)
        return {"summary": summary_text}
    except Exception as e:
        logger.error(f"Error in summary_generation_node: {e}")
        return {"errors": [f"Summary generation error: {str(e)}"]}


async def interview_questions_node(state: ScreenResumeState) -> Dict[str, Any]:
    """Generate custom interview questions based on candidate profile and gaps."""
    logger.info("Executing interview_questions_node...")
    try:
        desc = state.get("job_description", "")
        raw_text = state.get("resume_raw_text", "")
        gap = state.get("skill_gap") or {}
        
        q_data = await question_gen.generate_questions(desc, raw_text, gap)
        return {"suggested_questions": q_data.get("questions", [])}
    except Exception as e:
        logger.error(f"Error in interview_questions_node: {e}")
        return {"errors": [f"Interview questions error: {str(e)}"]}
