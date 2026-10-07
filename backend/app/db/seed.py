import logging
import uuid
from sqlalchemy import select
from app.db.database import AsyncSessionLocal
from app.models.organization import Organization
from app.models.user import User, UserRole
from app.models.job import Job, JobType, JobStatus
from app.models.candidate import Candidate, CandidateStatus, CandidateSkill
from app.models.skill import Skill
from app.models.resume import Resume
from app.models.match import MatchScore
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)

DEMO_ORG_NAME = "HireMind AI Technologies"
DEMO_USER_EMAIL = "rony.test@gmail.com"
DEMO_USER_PASSWORD = "Admin@1234"

async def seed_demo_data_if_needed():
    """Seed sample organization, user, open jobs, and candidates if database is empty."""
    async with AsyncSessionLocal() as session:
        try:
            # Check if demo user already exists
            user_stmt = select(User).where(User.email == DEMO_USER_EMAIL)
            result = await session.execute(user_stmt)
            existing_user = result.scalars().first()

            if existing_user:
                logger.info("Demo user already exists. Skipping database seeding.")
                return

            logger.info("Seeding demo organization, jobs, and candidates...")

            # 1. Create Organization
            org = Organization(id=uuid.uuid4(), name=DEMO_ORG_NAME)
            session.add(org)
            await session.flush()

            # 2. Create Demo User
            user = User(
                id=uuid.uuid4(),
                email=DEMO_USER_EMAIL,
                hashed_password=get_password_hash(DEMO_USER_PASSWORD),
                first_name="Rony",
                last_name="Mishra",
                role=UserRole.ADMIN,
                organization_id=org.id,
                is_active=True,
            )
            session.add(user)
            await session.flush()

            # 3. Create Skills
            skills_data = [
                "Python", "FastAPI", "React", "TypeScript", "PostgreSQL",
                "Redis", "Docker", "AWS", "Machine Learning", "System Design",
                "LangChain", "LLMs", "Kubernetes", "GraphQL"
            ]
            skill_map = {}
            for s_name in skills_data:
                sk = Skill(id=uuid.uuid4(), name=s_name)
                session.add(sk)
                skill_map[s_name] = sk
            await session.flush()

            # 4. Create Jobs
            job1 = Job(
                id=uuid.uuid4(),
                organization_id=org.id,
                title="Senior AI / LLM Engineer",
                description="Join our core AI team building production LLM RAG pipelines, autonomous agents, and scalable vector search architectures.",
                requirements="5+ years experience in Python, PyTorch/TensorFlow, FastAPI, LangGraph, Qdrant/Milvus, and cloud LLM integrations.",
                location="San Francisco, CA (Hybrid)",
                job_type=JobType.FULL_TIME,
                status=JobStatus.OPEN,
            )
            job2 = Job(
                id=uuid.uuid4(),
                organization_id=org.id,
                title="Full-Stack React & FastAPI Engineer",
                description="Looking for a high-velocity full-stack engineer proficient with modern React TypeScript UI, Redux, and FastAPI backends.",
                requirements="3+ years in React, TypeScript, Tailwind CSS, FastAPI, PostgreSQL, and WebSockets.",
                location="Remote",
                job_type=JobType.FULL_TIME,
                status=JobStatus.OPEN,
            )
            job3 = Job(
                id=uuid.uuid4(),
                organization_id=org.id,
                title="DevOps & Cloud Architect",
                description="Lead container orchestration, CI/CD pipelines, security, and cloud infrastructure monitoring across AWS & Kubernetes.",
                requirements="4+ years Docker, Terraform, Kubernetes, Helm, Prometheus, and AWS Cloud Security.",
                location="Austin, TX",
                job_type=JobType.FULL_TIME,
                status=JobStatus.OPEN,
            )
            session.add_all([job1, job2, job3])
            await session.flush()

            # 5. Create Candidates with Resumes & AI Matches
            c1 = Candidate(
                id=uuid.uuid4(),
                organization_id=org.id,
                first_name="Alex",
                last_name="Rivers",
                email="alex.rivers@example.com",
                phone="+1 (555) 234-5678",
                status=CandidateStatus.INTERVIEWING,
            )
            c2 = Candidate(
                id=uuid.uuid4(),
                organization_id=org.id,
                first_name="Sophia",
                last_name="Chen",
                email="sophia.chen@example.com",
                phone="+1 (555) 876-5432",
                status=CandidateStatus.SCREENING,
            )
            c3 = Candidate(
                id=uuid.uuid4(),
                organization_id=org.id,
                first_name="Marcus",
                last_name="Vance",
                email="marcus.vance@example.com",
                phone="+1 (555) 345-6789",
                status=CandidateStatus.NEW,
            )
            session.add_all([c1, c2, c3])
            await session.flush()

            # Tag Candidate Skills
            for sk_name in ["Python", "FastAPI", "LLMs", "Docker", "PostgreSQL"]:
                session.add(CandidateSkill(candidate_id=c1.id, skill_id=skill_map[sk_name].id, proficiency="Expert"))
            for sk_name in ["React", "TypeScript", "Python", "FastAPI"]:
                session.add(CandidateSkill(candidate_id=c2.id, skill_id=skill_map[sk_name].id, proficiency="Advanced"))
            for sk_name in ["Docker", "AWS", "Kubernetes", "Redis"]:
                session.add(CandidateSkill(candidate_id=c3.id, skill_id=skill_map[sk_name].id, proficiency="Expert"))
            await session.flush()

            # Add Resumes
            r1 = Resume(
                id=uuid.uuid4(),
                candidate_id=c1.id,
                file_path="uploads/demo_alex_rivers.pdf",
                file_name="Alex_Rivers_Resume.pdf",
                raw_text="Alex Rivers - Senior AI & LLM Specialist with 6 years experience in Python, FastAPI, LangGraph, Qdrant vector databases, PyTorch, and deploying custom LLM models on AWS.",
                parsed_json={
                    "name": "Alex Rivers",
                    "email": "alex.rivers@example.com",
                    "skills": ["Python", "FastAPI", "LLMs", "LangChain", "Qdrant", "Docker", "AWS"],
                    "experience_years": 6,
                    "summary": "Experienced AI Systems Architect focused on LLM RAG pipelines and vector database optimization."
                },
                interview_questions={
                    "questions": [
                        {
                            "question": "How do you optimize vector database retrieval speeds for high-dimensional embedding search?",
                            "expected_answer": "Discuss HNSW index tuning, quantization techniques (PQ/SQ), and payload filtering.",
                            "category": "Technical",
                            "difficulty_level": "Senior"
                        },
                        {
                            "question": "Can you explain your approach to handling multi-turn conversational memory in LangGraph/LLM pipelines?",
                            "expected_answer": "Should detail checkpointing, state management, and context window compression.",
                            "category": "Architecture",
                            "difficulty_level": "Senior"
                        }
                    ]
                }
            )
            r2 = Resume(
                id=uuid.uuid4(),
                candidate_id=c2.id,
                file_path="uploads/demo_sophia_chen.pdf",
                file_name="Sophia_Chen_Resume.pdf",
                raw_text="Sophia Chen - Full-Stack Developer with 4 years hands-on experience building web applications with React, TypeScript, Redux Toolkit, Tailwind CSS, Python FastAPI, and PostgreSQL.",
                parsed_json={
                    "name": "Sophia Chen",
                    "email": "sophia.chen@example.com",
                    "skills": ["React", "TypeScript", "Python", "FastAPI", "Tailwind CSS", "PostgreSQL"],
                    "experience_years": 4,
                    "summary": "Product-focused full-stack developer with strong UI/UX design sensibilities and clean API architecture skills."
                }
            )
            session.add_all([r1, r2])
            await session.flush()

            # Add Match Scores
            m1 = MatchScore(
                id=uuid.uuid4(),
                job_id=job1.id,
                candidate_id=c1.id,
                resume_id=r1.id,
                score=94.5,
                fit_explanation="Exceptional fit for Senior AI / LLM Engineer. Proven expertise in Python, FastAPI, vector DBs, and LLM orchestration aligns directly with target role requirements.",
                skill_gap_analysis={
                    "matching_skills": ["Python", "FastAPI", "LLMs", "LangChain", "Docker", "AWS"],
                    "missing_skills": ["Kubernetes"],
                    "recommended_learning": ["Advanced Kubernetes Operator patterns"],
                    "hiring_recommendation": "Strongly Recommended for Immediate Technical Interview"
                }
            )
            m2 = MatchScore(
                id=uuid.uuid4(),
                job_id=job2.id,
                candidate_id=c2.id,
                resume_id=r2.id,
                score=88.0,
                fit_explanation="Great fit for Full-Stack React & FastAPI Engineer. Strong front-end mastery paired with solid async FastAPI backend experience.",
                skill_gap_analysis={
                    "matching_skills": ["React", "TypeScript", "Python", "FastAPI", "PostgreSQL"],
                    "missing_skills": ["WebSockets"],
                    "recommended_learning": ["Real-time state sync with WebSockets"],
                    "hiring_recommendation": "Recommended for Interview"
                }
            )
            session.add_all([m1, m2])

            await session.commit()
            logger.info("Database successfully seeded with demo data!")
        except Exception as e:
            await session.rollback()
            logger.error(f"Error seeding database: {e}")
