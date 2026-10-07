import apiClient from './axios';

export interface CandidateComparisonResult {
  top_recommendation: string;
  summary_verdict: string;
  comparisons: {
    candidate_name: string;
    key_strengths: string[];
    skill_gaps: string[];
    experience_level: string;
    fit_score: number;
    verdict: string;
  }[];
}

export interface InterviewQuestionItem {
  question: string;
  expected_answer: string;
  category: string;
  difficulty_level: string;
}

export const aiApi = {
  compareCandidates: async (candidates: any[], jobDescription?: string): Promise<CandidateComparisonResult> => {
    const response = await apiClient.post<CandidateComparisonResult>('/ai/compare', {
      job_description: jobDescription || 'Target Engineering Role',
      candidates: candidates.map((c) => ({
        id: c.id,
        name: `${c.first_name} ${c.last_name}`,
        email: c.email,
        status: c.status,
        score: c.match_scores?.[0]?.score || null,
        skills: c.candidate_skills?.map((cs: any) => cs.skill?.name).filter(Boolean) || [],
        summary: c.resumes?.[0]?.parsed_json?.summary || 'Applicant candidate profile',
      })),
    });
    return response.data;
  },

  generateQuestions: async (jobDescription: string, resumeText: string, skillGaps?: any): Promise<{ questions: InterviewQuestionItem[] }> => {
    const response = await apiClient.post<{ questions: InterviewQuestionItem[] }>('/ai/questions', {
      job_description: jobDescription,
      resume_text: resumeText,
      skill_gaps: skillGaps || {},
    });
    return response.data;
  },

  seedDemoData: async (): Promise<void> => {
    await apiClient.post('/seed');
  },
};
