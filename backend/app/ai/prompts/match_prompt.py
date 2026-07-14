RESUME_MATCHING_PROMPT = """
You are a Principal Talent Acquisition Partner.
Compare the candidate's resume content against the Job Description details (title, description, and requirements).

Job Description:
Title: {job_title}
Description: {job_description}
Requirements: {job_requirements}

Candidate Resume:
{resume_text}

Calculate a match score between 0.0 and 100.0. Provide skill alignment metrics, experience fit, education fit, and a clear recommendation.

You MUST return a JSON object with this schema:
{{
  "score": float,
  "matching_skills": ["string"],
  "missing_skills": ["string"],
  "experience_match": "string",
  "education_match": "string",
  "hiring_recommendation": "string"
}}

Rules:
- Output ONLY valid JSON.
- Be objective and thorough.
"""

SKILL_GAP_PROMPT = """
Analyze the candidate's skill matrix against the Job Requirements.

Job Requirements:
{job_requirements}

Candidate Skills:
{candidate_skills}

Determine the missing skills, learning recommendations, priority skills, and candidate strengths and weaknesses.

You MUST return a JSON object with this schema:
{{
  "missing_skills": ["string"],
  "recommended_learning": ["string"],
  "priority_skills": ["string"],
  "strengths": ["string"],
  "weaknesses": ["string"]
}}

Rules:
- Output ONLY valid JSON.
"""
