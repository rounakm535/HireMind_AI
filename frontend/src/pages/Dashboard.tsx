import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../hooks';
import { fetchDashboardStats } from '../redux/slices/dashboardSlice';
import { fetchCandidates } from '../redux/slices/candidateSlice';
import PageHeader from '../components/layout/PageHeader';
import StatsCard from '../components/dashboard/StatsCard';
import RecentCandidates from '../components/dashboard/RecentCandidates';
import HiringPipeline from '../components/dashboard/HiringPipeline';
import SkillChart from '../components/dashboard/SkillChart';
import Loader from '../components/common/Loader';
import { Briefcase, Users, RefreshCw, BarChart } from 'lucide-react';
import Button from '../components/common/Button';

const Dashboard: React.FC = () => {
  const dispatch = useAppDispatch();
  const { stats, loading } = useAppSelector((state) => state.dashboard);
  const { candidates } = useAppSelector((state) => state.candidates);

  const loadData = () => {
    dispatch(fetchDashboardStats());
    dispatch(fetchCandidates({ size: 5 }));
  };

  useEffect(() => {
    loadData();
  }, [dispatch]);

  if (loading && !stats) {
    return (
      <div className="h-[70vh] w-full flex items-center justify-center">
        <Loader size="lg" className="text-brand-500" />
      </div>
    );
  }

  // Fallback defaults for dashboard values
  const totalJobs = stats?.total_jobs ?? 0;
  const totalCandidates = stats?.total_candidates ?? 0;
  const activeScreenings = stats?.active_screenings ?? 0;

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Recruitment Dashboard" subtitle="Overview of your current hiring progress and candidate fits.">
        <Button variant="outline" size="sm" onClick={loadData} className="gap-1.5 h-9">
          <RefreshCw size={14} />
          <span>Refresh</span>
        </Button>
      </PageHeader>

      {/* Stats Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard title="Active Job Openings" value={totalJobs} icon={Briefcase} color="brand" description="Currently open roles" />
        <StatsCard title="Total Candidates" value={totalCandidates} icon={Users} color="info" description="Across all funnel stages" />
        <StatsCard title="AI Resumes Screenings" value={activeScreenings} icon={BarChart} color="success" description="Completed fit calculations" />
      </div>

      {/* Middle Row: Recent Candidates & Hiring Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentCandidates candidates={candidates} />
        <HiringPipeline />
      </div>

      {/* Skill Stats Row */}
      <div className="grid grid-cols-1 gap-6">
        <SkillChart />
      </div>
    </div>
  );
};

export default Dashboard;
