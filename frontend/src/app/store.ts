import { configureStore } from '@reduxjs/toolkit';
import authReducer from '../redux/slices/authSlice';
import jobReducer from '../redux/slices/jobSlice';
import candidateReducer from '../redux/slices/candidateSlice';
import dashboardReducer from '../redux/slices/dashboardSlice';
import chatReducer from '../redux/slices/chatSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    jobs: jobReducer,
    candidates: candidateReducer,
    dashboard: dashboardReducer,
    chat: chatReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
