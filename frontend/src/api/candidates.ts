import apiClient from './axios';
import { Candidate, CandidateStatus } from '../types';
import { PaginatedResponse } from './jobs';

export interface GetCandidatesParams {
  page?: number;
  size?: number;
  status?: CandidateStatus;
  search?: string;
}

export const candidatesApi = {
  getCandidates: async (params: GetCandidatesParams): Promise<PaginatedResponse<Candidate>> => {
    const response = await apiClient.get<PaginatedResponse<Candidate>>('/candidates/', { params });
    return response.data;
  },

  getCandidate: async (id: string): Promise<Candidate> => {
    const response = await apiClient.get<Candidate>(`/candidates/${id}`);
    return response.data;
  },

  createCandidate: async (data: any): Promise<Candidate> => {
    const response = await apiClient.post<Candidate>('/candidates/', data);
    return response.data;
  },

  updateCandidate: async (id: string, data: any): Promise<Candidate> => {
    const response = await apiClient.put<Candidate>(`/candidates/${id}`, data);
    return response.data;
  },

  deleteCandidate: async (id: string): Promise<void> => {
    await apiClient.delete(`/candidates/${id}`);
  },
};
