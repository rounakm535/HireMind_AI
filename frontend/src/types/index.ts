export type UserRole = 'ADMIN' | 'RECRUITER' | 'HIRING_MANAGER';

export type JobType = 'FULL_TIME' | 'PART_TIME' | 'CONTRACT' | 'INTERN' | 'REMOTE';

export type JobStatus = 'DRAFT' | 'OPEN' | 'CLOSED';

export type CandidateStatus = 'NEW' | 'SCREENING' | 'INTERVIEWING' | 'OFFERED' | 'HIRED' | 'REJECTED';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  organization_id: string | null;
  is_active: boolean;
}

export interface Organization {
  id: string;
  name: string;
}

export interface Skill {
  id: string;
  name: string;
}

export interface CandidateSkill {
  skill: Skill;
  proficiency: string | null;
}

export interface Candidate {
  id: string;
  organization_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string | null;
  status: CandidateStatus;
  candidate_skills: CandidateSkill[];
  resumes?: Resume[];
  match_scores?: MatchScore[];
  created_at: string;
  updated_at: string;
}

export interface Job {
  id: string;
  organization_id: string;
  title: string;
  description: string;
  requirements: string;
  location: string;
  job_type: JobType;
  status: JobStatus;
  created_at: string;
  updated_at: string;
}

export interface Resume {
  id: string;
  candidate_id: string;
  file_url: string;
  file_name: string;
  parsed_content: any | null;
  raw_text: string | null;
  summary: string | null;
  interview_questions?: InterviewQuestion[];
  created_at: string;
  updated_at: string;
}

export interface InterviewQuestion {
  id: string;
  resume_id: string;
  question: string;
  expected_answer: string | null;
  category: string | null;
}

export interface MatchScore {
  id: string;
  job_id: string;
  candidate_id: string;
  resume_id: string;
  score: number;
  fit_explanation: string | null;
  skill_gap_analysis: {
    matched_skills: string[];
    missing_skills: string[];
    additional_skills: string[];
  } | null;
  created_at: string;
}

export interface EmailLog {
  id: string;
  sender_id: string | null;
  recipient_email: string;
  subject: string;
  body: string;
  status: 'SENT' | 'FAILED' | 'PENDING';
  created_at: string;
}

export interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: string;
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
