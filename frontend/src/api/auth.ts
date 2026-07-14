import apiClient from './axios';
import { User, Token } from '../types';

export const authApi = {
  login: async (email: string, password: string): Promise<Token> => {
    const response = await apiClient.post<Token>('/auth/login', { email, password });
    return response.data;
  },

  register: async (data: any): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', data);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me');
    return response.data;
  },
  
  refreshToken: async (token: string): Promise<Token> => {
    const response = await apiClient.post<Token>('/auth/refresh', { refresh_token: token });
    return response.data;
  }
};
