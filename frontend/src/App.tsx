import React, { Suspense, lazy, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from './hooks';
import { fetchCurrentUser } from './redux/slices/authSlice';
import ProtectedRoute from './routes/ProtectedRoute';
import Loader from './components/common/Loader';

// Lazy Loaded Pages
const Login = lazy(() => import('./pages/Login'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const JobList = lazy(() => import('./pages/jobs/JobList'));
const CreateJob = lazy(() => import('./pages/jobs/CreateJob'));
const EditJob = lazy(() => import('./pages/jobs/EditJob'));
const CandidateList = lazy(() => import('./pages/candidates/CandidateList'));
const CandidateProfile = lazy(() => import('./pages/candidates/CandidateProfile'));
const UploadResume = lazy(() => import('./pages/resume/UploadResume'));
const RecruiterChat = lazy(() => import('./pages/chat/RecruiterChat'));
const GenerateEmail = lazy(() => import('./pages/emails/GenerateEmail'));
const Analytics = lazy(() => import('./pages/analytics/Analytics'));

// Layout Shell (We will build it)
const AppLayout = lazy(() => import('./components/layout/AppLayout'));

const App: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isAuthenticated, user } = useAppSelector((state) => state.auth);

  useEffect(() => {
    if (isAuthenticated && !user) {
      dispatch(fetchCurrentUser());
    }
  }, [isAuthenticated, user, dispatch]);

  return (
    <Suspense fallback={<div className="h-screen w-screen flex items-center justify-center"><Loader size="lg" /></div>}>
      <Routes>
        {/* Public Route */}
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" replace />} />

        {/* Private Routes */}
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/jobs" element={<JobList />} />
            <Route path="/jobs/new" element={<CreateJob />} />
            <Route path="/jobs/:id" element={<EditJob />} />
            <Route path="/candidates" element={<CandidateList />} />
            <Route path="/candidates/:id" element={<CandidateProfile />} />
            <Route path="/resume/upload" element={<UploadResume />} />
            <Route path="/chat" element={<RecruiterChat />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/emails" element={<GenerateEmail />} />
          </Route>
        </Route>

        {/* 404 Route */}
        <Route
          path="*"
          element={
            <div className="h-screen flex flex-col items-center justify-center bg-brand-50 font-sans">
              <h1 className="text-6xl font-bold text-brand-600 mb-2">404</h1>
              <p className="text-xl text-slate-500 mb-6 font-medium">Page not found</p>
              <a
                href="/dashboard"
                className="px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white rounded-lg shadow-sm font-semibold transition"
              >
                Go Dashboard
              </a>
            </div>
          }
        />
      </Routes>
    </Suspense>
  );
};

export default App;
