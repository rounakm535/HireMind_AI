import React, { useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchDashboardStats } from '../../redux/slices/dashboardSlice';
import PageHeader from '../../components/layout/PageHeader';
import StatsCard from '../../components/dashboard/StatsCard';
import HiringPipeline from '../../components/dashboard/HiringPipeline';
import SkillChart from '../../components/dashboard/SkillChart';
import Button from '../../components/common/Button';
import { BarChart, Clock, TrendingUp, Download, Sparkles, CheckCircle2, Award } from 'lucide-react';

const Analytics: React.FC = () => {
  const dispatch = useAppDispatch();
  const { stats } = useAppSelector((state) => state.dashboard);

  useEffect(() => {
    dispatch(fetchDashboardStats());
  }, [dispatch]);

  const handleExportCSV = () => {
    const data = [
      ['Metric', 'Value'],
      ['Total Open Jobs', stats?.total_jobs || 0],
      ['Total Candidates', stats?.total_candidates || 0],
      ['Active AI Screenings', stats?.active_screenings || 0],
      ['Average Time to Hire', '14 Days'],
      ['Match Score Average', '84.2%'],
      ['AI Screening Accuracy', '99.1%'],
    ];

    const csvContent = 'data:text/csv;charset=utf-8,' + data.map((e) => e.join(',')).join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'hiremind_recruitment_analytics.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader
        title="Recruitment Analytics & Insights"
        subtitle="Real-time performance metrics, pipeline conversions, and AI screening throughput."
      >
        <Button variant="outline" size="sm" onClick={handleExportCSV} className="gap-1.5 h-9 font-semibold">
          <Download size={15} />
          <span>Export CSV Report</span>
        </Button>
      </PageHeader>

      {/* Row 1 Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <StatsCard
          title="Average Time to Hire"
          value="14 Days"
          icon={Clock}
          color="info"
          description="-3 Days improvement vs last month"
        />
        <StatsCard
          title="Candidate Match Ratio"
          value="84.2%"
          icon={TrendingUp}
          color="success"
          description="+6.4% higher skill alignment"
        />
        <StatsCard
          title="AI Parser Accuracy"
          value="99.1%"
          icon={BarChart}
          color="brand"
          description="Verified schema extraction score"
        />
        <StatsCard
          title="Interview Conversion"
          value="42%"
          icon={Award}
          color="warning"
          description="Screened to interview pass rate"
        />
      </div>

      {/* Main Analysis Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <HiringPipeline />
        <SkillChart />
      </div>

      {/* AI Performance Breakdown Banner */}
      <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm font-sans space-y-4">
        <div className="flex items-center gap-2 text-brand-600 font-bold text-sm">
          <Sparkles size={18} />
          <span>HireMind AI Screening Efficiency Breakdown</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 space-y-1">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Manual Resume Screening Saved</span>
            <div className="text-2xl font-black text-slate-800">142+ Hours</div>
            <p className="text-[11px] text-slate-500">Based on 12 mins saved per candidate resume parsed.</p>
          </div>

          <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 space-y-1">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Top Required Skill</span>
            <div className="text-2xl font-black text-slate-800">Python & AI/LLMs</div>
            <p className="text-[11px] text-slate-500">Required in 78% of active technical job descriptions.</p>
          </div>

          <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 space-y-1">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Candidate Quality Index</span>
            <div className="text-2xl font-black text-emerald-600 flex items-center gap-1">
              <CheckCircle2 size={20} />
              <span>9.4 / 10</span>
            </div>
            <p className="text-[11px] text-slate-500">Recruiter rating on AI candidate shortlist recommendations.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
