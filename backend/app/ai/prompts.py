# Prompts for AI processing in HireMind AI ATS

RESUME_PARSING_PROMPT = """
You are an expert ATS resume parser. Your job is to extract candidate information from the raw resume text.
Extract the details into a structured format containing:
- candidate_info: first name, last name, email, phone
- skills: list of technical and soft skills identified
- experience: list of work experiences (job title, company, dates, description)
- education: list of educational degrees (degree, school, field of study, graduation year)
- summary: a short professional summary of the candidate

Raw Resume Text:
{raw_text}

Return ONLY a valid JSON object matching this structure. Do not wrap in markdown code fences or include explanations.
"""

RESUME_MATCHING_PROMPT = """
You are a Staff Recruiter. Compare the candidate's resume summary and experience against the Job Description.
Calculate a match score from 0.0 to 100.0 based on how well the candidate's skills and experience align with the requirements.
Provide a clear fit explanation explaining why this score was given, highlighting strengths and weaknesses.

Job Description:
Title: {job_title}
Requirements: {job_requirements}
Description: {job_description}

Resume Content:
{resume_text}

Return ONLY a valid JSON object with keys:
- score (float)
- fit_explanation (string)
"""

SKILL_GAP_PROMPT = """
Analyze the candidate's skills list against the job requirements.
Identify:
- matched_skills: skills the candidate has that are required
- missing_skills: skills required or preferred by the job description but not explicitly found in the resume
- additional_skills: skills the candidate has that are not mentioned in the job description but are relevant

Job Requirements:
{job_requirements}

Candidate Skills:
{candidate_skills}

Return ONLY a valid JSON object with keys:
- matched_skills (list of strings)
- missing_skills (list of strings)
- additional_skills (list of strings)
"""

CANDIDATE_RANKING_PROMPT = """
Compare a list of candidates' summaries and matching scores for the job. Rank them from best to worst fit.
Provide a reasoning for the ranking order.

Job Description:
{job_description}

Candidates list (id, name, score, summary):
{candidates_list}

Return ONLY a valid JSON object with keys:
- rankings: list of candidate IDs in rank order
- reasoning: overall ranking explanation
"""

INTERVIEW_QUESTION_PROMPT = """
Generate a list of custom, targeted interview questions for the candidate based on their resume and identified skill gaps.
For each question, category (technical, behavioral, fit) and expected answer key should be generated.

Job Description:
{job_description}

Resume Content:
{resume_text}

Skill Gaps identified:
{skill_gaps}

Return ONLY a valid JSON object with keys:
- questions: list of objects, each with 'question', 'expected_answer', and 'category'
"""

SUMMARY_GENERATOR_PROMPT = """
Create a professional candidate profile summary for recruiters. Highlight key accomplishments, career focus, and fit highlights.

Resume Content:
{resume_text}

Return a concise candidate executive summary text.
"""
