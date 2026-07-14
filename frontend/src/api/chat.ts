import apiClient from './axios';

export interface ChatResponse {
  response: string;
}

export const chatApi = {
  sendMessage: async (query: string): Promise<ChatResponse> => {
    const response = await apiClient.post<ChatResponse>('/chat/', { query });
    return response.data;
  },
};
