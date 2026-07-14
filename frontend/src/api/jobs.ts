import apiClient from './axios';
import { Job, JobType, JobStatus } from '../types';

export interface GetJobsParams {
  page?: number;
  size?: number;
  job_type?: JobType;
  status?: JobStatus;
  search?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export const jobsApi = {
  getJobs: async (params: GetJobsParams): Promise<PaginatedResponse<Job>> => {
    const response = await apiClient.get<PaginatedResponse<Job>>('/jobs/', { params });
    return response.data;
  },

  getJob: async (id: string): Promise<Job> => {
    const response = await apiClient.get<Job>(`/jobs/${id}`);
    return response.data;
  },

  createJob: async (data: any): Promise<Job> => {
    const response = await apiClient.post<Job>('/jobs/', data);
    return response.data;
  },

  updateJob: async (id: string, data: any): Promise<Job> => {
    const response = await apiClient.put<Job>(`/jobs/${id}`, data);
    return response.data;
  },

  deleteJob: async (id: string): Promise<void> => {
    await apiClient.delete(`/jobs/${id}`);
  },
};
