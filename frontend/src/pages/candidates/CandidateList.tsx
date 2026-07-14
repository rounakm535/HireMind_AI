import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchCandidates } from '../../redux/slices/candidateSlice';
import PageHeader from '../../components/layout/PageHeader';
import SearchBar from '../../components/common/SearchBar';
import Select from '../../components/common/Select';
import Pagination from '../../components/common/Pagination';
import CandidateCard from '../../components/candidates/CandidateCard';
import CandidateTable from '../../components/candidates/CandidateTable';
import Loader from '../../components/common/Loader';
import Button from '../../components/common/Button';
import { Upload, LayoutGrid, List } from 'lucide-react';
import { CandidateStatus } from '../../types';

const CandidateList: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { candidates, loading, totalPages, currentPage } = useAppSelector((state) => state.candidates);

  // States
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<string>('ALL');

  const loadCandidates = (page: number = 1) => {
    const params: any = {
      page,
      size: 10,
    };
    if (search) params.search = search;
    if (status !== 'ALL') params.status = status as CandidateStatus;

    dispatch(fetchCandidates(params));
  };

  useEffect(() => {
    loadCandidates(1);
  }, [search, status, dispatch]);

  const statusOptions = [
    { value: 'ALL', label: 'All Statuses' },
    { value: 'NEW', label: 'New' },
    { value: 'SCREENING', label: 'Screening' },
    { value: 'INTERVIEWING', label: 'Interviewing' },
    { value: 'OFFERED', label: 'Offered' },
    { value: 'HIRED', label: 'Hired' },
    { value: 'REJECTED', label: 'Rejected' },
  ];

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Candidate Database" subtitle="Browse, search, and screen applicant records.">
        <Button variant="primary" size="sm" onClick={() => navigate('/resume/upload')} className="gap-1.5 h-9">
          <Upload size={16} />
          <span>Upload Resume</span>
        </Button>
      </PageHeader>

      {/* Filter Toolbar */}
      <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <SearchBar placeholder="Search candidates by name or email..." onSearch={(q) => setSearch(q)} />

        <div className="flex flex-wrap items-center gap-3.5">
          <div className="w-44">
            <Select
              options={statusOptions}
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            />
          </div>

          {/* Toggle View */}
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

      {/* Rendering content */}
      {loading ? (
        <div className="h-[40vh] w-full flex items-center justify-center">
          <Loader size="lg" className="text-brand-500" />
        </div>
      ) : candidates.length === 0 ? (
        <div className="text-center py-16 bg-white border border-slate-100 rounded-2xl">
          <p className="text-slate-400 text-sm">No candidate records found matching your filters.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {candidates.map((candidate) => (
            <CandidateCard key={candidate.id} candidate={candidate} />
          ))}
        </div>
      ) : (
        <CandidateTable candidates={candidates} />
      )}

      {/* Pagination */}
      <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={loadCandidates} />
    </div>
  );
};

export default CandidateList;
