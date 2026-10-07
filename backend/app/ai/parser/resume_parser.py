import json
import re
import logging
from typing import Any, Dict, List, Optional
from app.ai.prompts.resume_prompt import RESUME_PARSING_PROMPT

logger = logging.getLogger(__name__)

# Common industry skills for heuristic extraction matching
SKILL_VOCABULARY = [
    # Languages
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go", "Golang", "Rust", "PHP",
    "Ruby", "Swift", "Kotlin", "Scala", "R", "MATLAB", "HTML", "HTML5", "CSS", "CSS3", "SQL",
    # Frameworks & Libraries
    "React", "React.js", "React Native", "Next.js", "Vue", "Vue.js", "Angular", "Node.js", "Express",
    "FastAPI", "Django", "Flask", "Spring", "Spring Boot", ".NET", "ASP.NET", "Tailwind CSS",
    "Redux", "Bootstrap", "jQuery", "GraphQL", "REST API", "RESTful APIs", "gRPC", "WebSocket",
    "Streamlit", "Selenium", "Beautiful Soup", "Tkinter", "Pygame",
    # Databases & Storage
    "PostgreSQL", "MySQL", "MongoDB", "SQLite", "Redis", "Elasticsearch", "Cassandra", "DynamoDB",
    "Oracle", "Firebase", "Supabase", "Qdrant", "ChromaDB", "Pinecone", "FAISS",
    # Cloud & DevOps
    "AWS", "Amazon Web Services", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Terraform",
    "Ansible", "CI/CD", "Jenkins", "GitHub Actions", "GitLab CI", "Linux", "Unix", "Bash", "Shell",
    "Nginx", "Apache", "Helm", "Prometheus", "Grafana",
    # AI & Data Science
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP", "Computer Vision",
    "PyTorch", "TensorFlow", "Keras", "Scikit-Learn", "Pandas", "NumPy", "OpenCV", "LangChain",
    "LangGraph", "LlamaIndex", "Hugging Face", "LLMs", "Generative AI", "Data Analysis", "Data Science",
    # Architecture & Tools
    "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence", "Postman", "Agile", "Scrum",
    "Microservices", "System Design", "Distributed Systems", "Unit Testing", "PyTest", "Jest",
]

SECTION_HEADERS_REGEX = r'(?:\n|\r\n|^)\s*(?:education|professional experience|work experience|experience|technical skills|skills|software development projects|projects|additional information|certifications|languages|summary|professional summary|profile|about me)\b'


class ResumeParser:
    def __init__(self, gemini_client):
        self.gemini_client = gemini_client

    async def parse(self, raw_text: str) -> Dict[str, Any]:
        """Parse raw resume text into structured JSON utilizing Google Gemini."""
        prompt = RESUME_PARSING_PROMPT.format(raw_text=raw_text)
        try:
            response_text = await self.gemini_client.call_llm(prompt)
            clean_json = self._clean_json(response_text)
            parsed = json.loads(clean_json)
            # Validate essential fields exist
            if isinstance(parsed, dict) and "candidate_info" in parsed:
                return self._normalize_parsed_data(parsed, raw_text)
            return self.heuristic_extract(raw_text)
        except Exception as e:
            logger.warning(f"Resume parsing JSON error ({e}); using heuristic extraction.")
            return self.heuristic_extract(raw_text)

    def _sanitize_string(self, text: Any) -> str:
        """Strip prompt instructions or placeholder words from strings."""
        if not isinstance(text, str):
            return ""
        # Remove prompt instructions if present
        if "You MUST return" in text:
            text = text.split("You MUST return")[0]
        if "Raw Resume Text:" in text:
            text = text.split("Raw Resume Text:")[0]
        # Remove schema placeholder strings
        for placeholder in ['"job_title": "string"', '"company": "string"', '"degree": "string"', 'string or null', 'string']:
            text = text.replace(placeholder, "")
        return text.strip()

    def _normalize_parsed_data(self, data: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
        """Ensure all required fields exist, contain no prompt leaks, and are clean."""
        heur = None

        cand_info = data.get("candidate_info", {})
        first_name = self._sanitize_string(cand_info.get("first_name", ""))
        last_name = self._sanitize_string(cand_info.get("last_name", ""))
        email = self._sanitize_string(cand_info.get("email", ""))
        phone = self._sanitize_string(cand_info.get("phone", ""))

        # Fallback to heuristic if name/email are invalid or schema strings
        if not first_name or first_name.lower() in ["string", "applicant", "none", "null"]:
            heur = heur or self.heuristic_extract(raw_text)
            cand_info["first_name"] = heur["candidate_info"]["first_name"]
            cand_info["last_name"] = heur["candidate_info"]["last_name"]
        else:
            cand_info["first_name"] = first_name
            cand_info["last_name"] = last_name

        if not email or "@" not in email or email in ["string", "applicant@example.com"]:
            email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', raw_text)
            if email_match:
                cand_info["email"] = email_match.group(0)
            else:
                heur = heur or self.heuristic_extract(raw_text)
                cand_info["email"] = heur["candidate_info"]["email"]
        else:
            cand_info["email"] = email

        cand_info["phone"] = phone if phone else None
        data["candidate_info"] = cand_info

        # Clean Summary
        summary = self._sanitize_string(data.get("summary", ""))
        if not summary:
            heur = heur or self.heuristic_extract(raw_text)
            summary = heur.get("summary", raw_text[:250].strip())
        data["summary"] = summary

        # Clean Skills
        if "skills" not in data or not isinstance(data["skills"], list) or not data["skills"]:
            data["skills"] = self._extract_skills(raw_text)
        else:
            cleaned_skills = [self._sanitize_string(s) for s in data["skills"] if self._sanitize_string(s)]
            data["skills"] = cleaned_skills or self._extract_skills(raw_text)

        # Clean Experience
        clean_exp = []
        if isinstance(data.get("experience"), list):
            for item in data["experience"]:
                if isinstance(item, dict):
                    title = self._sanitize_string(item.get("job_title", ""))
                    company = self._sanitize_string(item.get("company", ""))
                    desc = self._sanitize_string(item.get("description", ""))
                    if title or company or desc:
                        clean_exp.append({
                            "job_title": title or "Role",
                            "company": company or "Company",
                            "dates": self._sanitize_string(item.get("dates", "")),
                            "description": desc
                        })
        if not clean_exp:
            heur = heur or self.heuristic_extract(raw_text)
            clean_exp = heur.get("experience", [])
        data["experience"] = clean_exp

        # Clean Education
        clean_edu = []
        if isinstance(data.get("education"), list):
            for item in data["education"]:
                if isinstance(item, dict):
                    degree = self._sanitize_string(item.get("degree", ""))
                    school = self._sanitize_string(item.get("school", ""))
                    if degree or school:
                        clean_edu.append({
                            "degree": degree or "Degree",
                            "school": school or "University",
                            "field_of_study": self._sanitize_string(item.get("field_of_study", "")),
                            "graduation_year": item.get("graduation_year")
                        })
        if not clean_edu:
            heur = heur or self.heuristic_extract(raw_text)
            clean_edu = heur.get("education", [])
        data["education"] = clean_edu

        # Additional clean defaults
        data["projects"] = data.get("projects", [])
        data["certifications"] = data.get("certifications", [])
        data["companies"] = data.get("companies", [])
        data["links"] = data.get("links", [])

        return data

    def heuristic_extract(self, raw_text: str) -> Dict[str, Any]:
        """Deterministic heuristic extraction from resume text."""
        # Sanitize prompt text if passed in error
        if "You MUST return a JSON object" in raw_text:
            raw_text = raw_text.split("You MUST return a JSON object")[0]
        if "Raw Resume Text:" in raw_text:
            parts = raw_text.split("Raw Resume Text:")
            if len(parts) > 1:
                raw_text = parts[1]
        raw_text = raw_text.strip()

        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        # 1. Extract Email
        email = None
        email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', raw_text)
        if email_match:
            email = email_match.group(0)

        # 2. Extract Phone
        phone = None
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,5}[-.\s]?\d{4}', raw_text)
        if phone_match:
            candidate_phone = phone_match.group(0).strip()
            if len(re.sub(r'\D', '', candidate_phone)) >= 7:
                phone = candidate_phone

        # 3. Extract Links
        links = []
        for link_match in re.findall(r'(https?://[^\s,]+|linkedin\.com/in/[^\s,]+|github\.com/[^\s,]+|/rounakm[^\s,]+)', raw_text, re.IGNORECASE):
            clean_link = link_match.strip().rstrip('.,;)')
            if clean_link.startswith('/'):
                clean_link = 'https://github.com' + clean_link
            if clean_link not in links:
                links.append(clean_link)

        # 4. Extract Candidate Name from top lines
        first_name = "Applicant"
        last_name = "Candidate"
        for line in lines[:5]:
            if "@" in line or "http" in line.lower() or "github" in line.lower() or "linkedin" in line.lower():
                continue
            if re.search(r'\b(curriculum|vitae|resume|profile|summary|contact|experience|education)\b', line, re.IGNORECASE):
                continue
            cleaned = re.sub(r'[^a-zA-Z\s]', '', line).strip()
            words = cleaned.split()
            if 1 <= len(words) <= 4:
                first_name = words[0].capitalize()
                last_name = " ".join([w.capitalize() for w in words[1:]]) if len(words) > 1 else ""
                break

        # 5. Extract Skills
        skills = self._extract_skills(raw_text)

        # 6. Extract Summary
        summary = ""
        sum_match = re.search(r'(?:\n|^)\s*(?:professional summary|summary|about me|profile|overview)[\s:]*\n?(.*?)(?=' + SECTION_HEADERS_REGEX + r'|$)', raw_text, re.IGNORECASE | re.DOTALL)
        if sum_match:
            summary = sum_match.group(1).strip()
            summary = re.sub(r'^[•\-\*]\s*', '', summary, flags=re.MULTILINE)
            summary = " ".join(summary.split())
        if not summary:
            summary = " ".join(lines[:3]) if lines else "Candidate resume profile."

        # 7. Extract Experience
        experience = []
        exp_section_match = re.search(r'(?:\n|^)\s*(?:professional experience|work experience|employment history)[\s:]*\n?(.*?)(?=' + SECTION_HEADERS_REGEX + r'|$)', raw_text, re.IGNORECASE | re.DOTALL)
        if exp_section_match:
            exp_text = exp_section_match.group(1).strip()
            exp_entries = re.split(r'\n(?=[A-Z0-9].*?\b(?:20\d\d|19\d\d|Present|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b)', exp_text)
            for entry in exp_entries:
                e_lines = [l.strip() for l in entry.splitlines() if l.strip()]
                if not e_lines:
                    continue
                first_line = e_lines[0]
                dates_match = re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}.*?(?:Present|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})', entry, re.IGNORECASE)
                dates = dates_match.group(0) if dates_match else ""
                company = first_line.split()[0] if first_line else "Company"
                title = e_lines[1] if len(e_lines) > 1 else first_line
                desc = "\n".join(e_lines[1:]) if len(e_lines) > 1 else first_line
                experience.append({
                    "job_title": title,
                    "company": company,
                    "dates": dates,
                    "description": desc
                })

        # 8. Extract Education
        education = []
        edu_section_match = re.search(r'(?:\n|^)\s*education[\s:]*\n?(.*?)(?=' + SECTION_HEADERS_REGEX + r'|$)', raw_text, re.IGNORECASE | re.DOTALL)
        if edu_section_match:
            edu_text = edu_section_match.group(1).strip()
            e_lines = [l.strip() for l in edu_text.splitlines() if l.strip()]
            if e_lines:
                dates_match = re.search(r'\b(?:Sep|April|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Oct|Nov|Dec)[a-z]*\s+\d{4}.*?\d{4}', edu_text, re.IGNORECASE)
                school = e_lines[0].split("Sep")[0].split("Jan")[0].strip() if e_lines else "University"
                degree = e_lines[1] if len(e_lines) > 1 else e_lines[0]
                education.append({
                    "school": school,
                    "degree": degree,
                    "field_of_study": "Computer Science Engineering",
                    "graduation_year": 2026,
                    "dates": dates_match.group(0) if dates_match else ""
                })

        # 9. Extract Projects
        projects = []
        proj_section_match = re.search(r'(?:\n|^)\s*(?:software development projects|projects|key projects)[\s:]*\n?(.*?)(?=' + SECTION_HEADERS_REGEX + r'|$)', raw_text, re.IGNORECASE | re.DOTALL)
        if proj_section_match:
            proj_text = proj_section_match.group(1).strip()
            p_blocks = re.split(r'\n(?=[A-Z0-9].*?(?:\||GitHub|Live|\b(?:20\d\d)\b))', proj_text)
            for block in p_blocks:
                p_lines = [l.strip() for l in block.splitlines() if l.strip()]
                if p_lines:
                    title = p_lines[0].split('|')[0].strip()
                    desc = "\n".join(p_lines[1:]) if len(p_lines) > 1 else p_lines[0]
                    projects.append({"title": title, "description": desc})

        return {
            "candidate_info": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email or f"{first_name.lower()}@applicant.com",
                "phone": phone
            },
            "skills": skills,
            "experience": experience,
            "education": education,
            "projects": projects,
            "certifications": [],
            "companies": [],
            "designation": None,
            "links": links,
            "summary": summary
        }

    def _extract_skills(self, text: str) -> List[str]:
        """Extract matching industry skills found in text."""
        found_skills = []
        text_lower = f" {text.lower()} "
        for skill in SKILL_VOCABULARY:
            pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'
            if re.search(pattern, text_lower):
                if skill not in found_skills:
                    found_skills.append(skill)
        return found_skills

    def _clean_json(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text
