import apiClient from './axios';

export interface DashboardStats {
  total_jobs: number;
  total_candidates: number;
  active_screenings: number;
  recent_activity: Array<{
    event: string;
    timestamp: string;
  }>;
}

export const dashboardApi = {
  getStats: async (): Promise<DashboardStats> => {
    const response = await apiClient.get<DashboardStats>('/dashboard/');
    return response.data;
  },
};
