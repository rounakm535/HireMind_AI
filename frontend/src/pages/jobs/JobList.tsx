import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchJobs, deleteJobPost } from '../../redux/slices/jobSlice';
import PageHeader from '../../components/layout/PageHeader';
import SearchBar from '../../components/common/SearchBar';
import Select from '../../components/common/Select';
import Pagination from '../../components/common/Pagination';
import JobCard from '../../components/jobs/JobCard';
import JobTable from '../../components/jobs/JobTable';
import Loader from '../../components/common/Loader';
import Button from '../../components/common/Button';
import { Plus, LayoutGrid, List } from 'lucide-react';
import { JobType, JobStatus } from '../../types';

const JobList: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { jobs, loading, totalPages, currentPage } = useAppSelector((state) => state.jobs);

  // States
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [search, setSearch] = useState('');
  const [jobType, setJobType] = useState<string>('ALL');
  const [status, setStatus] = useState<string>('ALL');

  const loadJobs = (page: number = 1) => {
    const params: any = {
      page,
      size: 10,
    };
    if (search) params.search = search;
    if (jobType !== 'ALL') params.job_type = jobType as JobType;
    if (status !== 'ALL') params.status = status as JobStatus;

    dispatch(fetchJobs(params));
  };

  useEffect(() => {
    loadJobs(1);
  }, [search, jobType, status, dispatch]);

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this job post?')) {
      dispatch(deleteJobPost(id));
    }
  };

  const jobTypeOptions = [
    { value: 'ALL', label: 'All Job Types' },
    { value: 'FULL_TIME', label: 'Full Time' },
    { value: 'PART_TIME', label: 'Part Time' },
    { value: 'CONTRACT', label: 'Contract' },
    { value: 'INTERN', label: 'Intern' },
    { value: 'REMOTE', label: 'Remote' },
  ];

  const statusOptions = [
    { value: 'ALL', label: 'All Statuses' },
    { value: 'DRAFT', label: 'Draft' },
    { value: 'OPEN', label: 'Open' },
    { value: 'CLOSED', label: 'Closed' },
  ];

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Job Openings" subtitle="Manage your team's available roles and positions.">
        <Button variant="primary" size="sm" onClick={() => navigate('/jobs/new')} className="gap-1.5 h-9">
          <Plus size={16} />
          <span>Post New Job</span>
        </Button>
      </PageHeader>

      {/* Search & Filter Controls */}
      <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <SearchBar placeholder="Search jobs by title or description..." onSearch={(q) => setSearch(q)} />
        
        <div className="flex flex-wrap items-center gap-3.5">
          <div className="w-40">
            <Select
              options={jobTypeOptions}
              value={jobType}
              onChange={(e) => setJobType(e.target.value)}
            />
          </div>
          <div className="w-40">
            <Select
              options={statusOptions}
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            />
          </div>

          {/* Toggle View mode */}
          <div className="flex border border-slate-200 rounded-lg p-1 bg-slate-50 gap-1 shrink-0">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-md transition ${
                viewMode === 'grid' ? 'bg-white text-brand-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'
              }`}
            >
              <LayoutGrid size={15} />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-md transition ${
                viewMode === 'table' ? 'bg-white text-brand-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'
              }`}
            >
              <List size={15} />
            </button>
          </div>
        </div>
      </div>

      {/* Content Rendering */}
      {loading ? (
        <div className="h-[40vh] w-full flex items-center justify-center">
          <Loader size="lg" className="text-brand-500" />
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-16 bg-white border border-slate-100 rounded-2xl">
          <p className="text-slate-400 text-sm">No job posts match your criteria.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} onDelete={handleDelete} />
          ))}
        </div>
      ) : (
        <JobTable jobs={jobs} onDelete={handleDelete} />
      )}

      {/* Pagination */}
      <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={loadJobs} />
    </div>
  );
};

export default JobList;
