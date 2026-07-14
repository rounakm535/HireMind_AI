import React from 'react';
import PageHeader from '../../components/layout/PageHeader';
import StatsCard from '../../components/dashboard/StatsCard';
import HiringPipeline from '../../components/dashboard/HiringPipeline';
import SkillChart from '../../components/dashboard/SkillChart';
import { BarChart, Clock, TrendingUp } from 'lucide-react';

const Analytics: React.FC = () => {
  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Recruitment Analytics" subtitle="Deep dive reports and statistics on screening throughput." />

      {/* Row 1 Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard title="Time to Hire Average" value="18 Days" icon={Clock} color="info" description="-2 Days from last month" />
        <StatsCard title="Application Match Ratio" value="76%" icon={TrendingUp} color="success" description="+4% increase in quality" />
        <StatsCard title="AI Parser Screenings" value="98.5%" icon={BarChart} color="brand" description="High accuracy score rating" />
      </div>

      {/* Grid Layout splits */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <HiringPipeline />
        <SkillChart />
      </div>
    </div>
  );
};

export default Analytics;
