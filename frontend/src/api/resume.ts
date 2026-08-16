import apiClient from './axios';
import { Resume, MatchScore, EmailLog } from '../types';

export const resumeApi = {
  uploadResume: async (candidateId: string | null | undefined, file: File): Promise<Resume> => {
    const formData = new FormData();
    if (candidateId) {
      formData.append('candidate_id', candidateId);
    }
    formData.append('file', file);

    const response = await apiClient.post<Resume>('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getResume: async (id: string): Promise<Resume> => {
    const response = await apiClient.get<Resume>(`/resumes/${id}`);
    return response.data;
  },

  deleteResume: async (id: string): Promise<void> => {
    await apiClient.delete(`/resumes/${id}`);
  },

  matchResume: async (resumeId: string, jobId: string): Promise<MatchScore> => {
    const response = await apiClient.post<MatchScore>('/resumes/match', null, {
      params: {
        resume_id: resumeId,
        job_id: jobId,
      },
    });
    return response.data;
  },

  getJobRankings: async (jobId: string): Promise<MatchScore[]> => {
    const response = await apiClient.get<MatchScore[]>(`/resumes/job-rankings/${jobId}`);
    return response.data;
  },

  generateEmail: async (candidateId: string, jobId: string, templateType: string): Promise<EmailLog> => {
    const response = await apiClient.post<EmailLog>('/emails/generate', {
      candidate_id: candidateId,
      job_id: jobId,
      template_type: templateType,
    });
    return response.data;
  },
};
