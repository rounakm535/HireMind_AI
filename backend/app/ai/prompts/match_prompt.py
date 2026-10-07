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

FULL_SCREENING_PROMPT = """
You are a Principal Talent Acquisition Partner and Technical Hiring Specialist.
Perform a thorough, comprehensive screening and match evaluation of the candidate's resume against the Job Description and requirements.

Job Details:
Title: {job_title}
Description: {job_description}
Requirements: {job_requirements}

Candidate Resume:
{resume_text}

Analyze the candidate's technical skills, past experience, and educational background relative to the job requirements.
Return a structured JSON object matching this exact schema:
{{
  "score": float,
  "fit_explanation": "Detailed 2-3 paragraph executive summary of why the candidate is or is not a strong fit for this specific position.",
  "matching_skills": ["string"],
  "missing_skills": ["string"],
  "additional_skills": ["string"],
  "strengths": ["string"],
  "weaknesses": ["string"],
  "recommended_learning": ["string"],
  "suggested_questions": [
    {{
      "question": "Targeted technical question based on their resume and job requirements",
      "expected_answer": "Key points candidate should cover",
      "category": "Technical",
      "difficulty_level": "Medium"
    }},
    {{
      "question": "Behavioral or architecture question",
      "expected_answer": "Key evaluation criteria",
      "category": "Behavioral",
      "difficulty_level": "Medium"
    }}
  ]
}}

Rules:
- Output ONLY valid JSON without markdown wrapping.
- Provide objective, realistic scoring and clear, actionable feedback.
"""
