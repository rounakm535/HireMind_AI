import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchCandidates, deleteCandidateProfile } from '../../redux/slices/candidateSlice';
import PageHeader from '../../components/layout/PageHeader';
import SearchBar from '../../components/common/SearchBar';
import Select from '../../components/common/Select';
import Pagination from '../../components/common/Pagination';
import CandidateCard from '../../components/candidates/CandidateCard';
import CandidateTable from '../../components/candidates/CandidateTable';
import EditCandidateModal from '../../components/candidates/EditCandidateModal';
import DeleteConfirmModal from '../../components/common/DeleteConfirmModal';
import SendEmailModal from '../../components/candidates/SendEmailModal';
import CandidateCompareModal from '../../components/candidates/CandidateCompareModal';
import Loader from '../../components/common/Loader';
import Button from '../../components/common/Button';
import { Upload, LayoutGrid, List, Sparkles, Database, CheckSquare, Square } from 'lucide-react';
import { Candidate, CandidateStatus } from '../../types';
import { aiApi } from '../../api/ai';

const CandidateList: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useAppDispatch();
  const { candidates, loading, totalPages, currentPage } = useAppSelector((state) => state.candidates);

  // States
  const [viewMode, setViewMode] = useState<'grid' | 'table'>('grid');
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState<string>('ALL');

  const [selectedCandidateIds, setSelectedCandidateIds] = useState<string[]>([]);
  const [isCompareModalOpen, setIsCompareModalOpen] = useState(false);

  const [selectedCandidateForEdit, setSelectedCandidateForEdit] = useState<Candidate | null>(null);
  const [selectedCandidateForDelete, setSelectedCandidateForDelete] = useState<Candidate | null>(null);
  const [selectedCandidateForEmail, setSelectedCandidateForEmail] = useState<Candidate | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [seeding, setSeeding] = useState(false);

  const loadCandidates = useCallback(
    (page: number = 1) => {
      const params: any = {
        page,
        size: 10,
      };
      if (search) params.search = search;
      if (status !== 'ALL') params.status = status as CandidateStatus;

      dispatch(fetchCandidates(params));
    },
    [search, status, dispatch]
  );

  useEffect(() => {
    loadCandidates(1);
  }, [loadCandidates]);

  const toggleSelectCandidate = (id: string) => {
    setSelectedCandidateIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleSeedData = async () => {
    setSeeding(true);
    try {
      await aiApi.seedDemoData();
      loadCandidates(1);
    } catch (err) {
      console.error('Failed to seed demo data:', err);
    } finally {
      setSeeding(false);
    }
  };

  const handleDeleteCandidate = async () => {
    if (!selectedCandidateForDelete) return;
    setDeleting(true);
    const res = await dispatch(deleteCandidateProfile(selectedCandidateForDelete.id));
    if (deleteCandidateProfile.fulfilled.match(res)) {
      loadCandidates(currentPage);
      setSelectedCandidateForDelete(null);
    }
    setDeleting(false);
  };

  const selectedCandidatesToCompare = candidates.filter((c) => selectedCandidateIds.includes(c.id));

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
      <PageHeader
        title="Candidate Database"
        subtitle="Browse, search, and screen applicant records with match scores, side-by-side comparisons, and direct emailing."
      >
        <div className="flex items-center gap-2">
          {selectedCandidateIds.length >= 2 && (
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setIsCompareModalOpen(true)}
              className="gap-1.5 h-9 bg-amber-500 hover:bg-amber-600 text-white font-bold"
            >
              <Sparkles size={15} />
              <span>Compare Selected ({selectedCandidateIds.length})</span>
            </Button>
          )}

          <Button variant="outline" size="sm" onClick={handleSeedData} isLoading={seeding} className="gap-1.5 h-9">
            <Database size={15} />
            <span>Load Demo Data</span>
          </Button>

          <Button variant="primary" size="sm" onClick={() => navigate('/resume/upload')} className="gap-1.5 h-9">
            <Upload size={16} />
            <span>Upload Resume</span>
          </Button>
        </div>
      </PageHeader>

      {/* Filter Toolbar */}
      <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <SearchBar placeholder="Search candidates by name or email..." onSearch={(q) => setSearch(q)} />

        <div className="flex flex-wrap items-center gap-3.5">
          <div className="w-44">
            <Select options={statusOptions} value={status} onChange={(e) => setStatus(e.target.value)} />
          </div>

          {/* Toggle View */}
          <div className="flex border border-slate-200 rounded-lg p-1 bg-slate-50 gap-1 shrink-0">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-md transition ${
                viewMode === 'grid' ? 'bg-white text-brand-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'
              }`}
              title="Grid View"
            >
              <LayoutGrid size={15} />
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-md transition ${
                viewMode === 'table' ? 'bg-white text-brand-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'
              }`}
              title="Table View"
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
        <div className="text-center py-16 bg-white border border-slate-100 rounded-2xl space-y-3">
          <p className="text-slate-400 text-sm">No candidate records found in your database.</p>
          <Button variant="primary" size="sm" onClick={handleSeedData} isLoading={seeding} className="gap-1.5">
            <Database size={15} />
            <span>Populate Sample Demo Candidates</span>
          </Button>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {candidates.map((candidate) => {
            const isSelected = selectedCandidateIds.includes(candidate.id);
            return (
              <div key={candidate.id} className="relative group">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleSelectCandidate(candidate.id);
                  }}
                  className={`absolute top-4 left-4 z-10 p-1.5 rounded-lg border transition ${
                    isSelected
                      ? 'bg-brand-600 text-white border-brand-600'
                      : 'bg-white/90 text-slate-400 border-slate-200 hover:border-brand-500'
                  }`}
                  title={isSelected ? 'Deselect candidate' : 'Select for comparison'}
                >
                  {isSelected ? <CheckSquare size={16} /> : <Square size={16} />}
                </button>
                <div className={isSelected ? 'ring-2 ring-brand-500 rounded-2xl' : ''}>
                  <CandidateCard
                    candidate={candidate}
                    onEdit={(c) => setSelectedCandidateForEdit(c)}
                    onDelete={(c) => setSelectedCandidateForDelete(c)}
                    onSendEmail={(c) => setSelectedCandidateForEmail(c)}
                  />
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <CandidateTable
          candidates={candidates}
          onEdit={(c) => setSelectedCandidateForEdit(c)}
          onDelete={(c) => setSelectedCandidateForDelete(c)}
          onSendEmail={(c) => setSelectedCandidateForEmail(c)}
        />
      )}

      {/* Pagination */}
      <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={loadCandidates} />

      {/* Comparison Modal */}
      {isCompareModalOpen && (
        <CandidateCompareModal
          isOpen={isCompareModalOpen}
          onClose={() => setIsCompareModalOpen(false)}
          candidates={selectedCandidatesToCompare}
          onSendEmail={(c) => setSelectedCandidateForEmail(c)}
        />
      )}

      {/* Edit Modal */}
      {selectedCandidateForEdit && (
        <EditCandidateModal
          isOpen={Boolean(selectedCandidateForEdit)}
          onClose={() => setSelectedCandidateForEdit(null)}
          candidate={selectedCandidateForEdit}
          onSuccess={() => loadCandidates(currentPage)}
        />
      )}

      {/* Direct Email Modal */}
      {selectedCandidateForEmail && (
        <SendEmailModal
          isOpen={Boolean(selectedCandidateForEmail)}
          onClose={() => setSelectedCandidateForEmail(null)}
          candidate={selectedCandidateForEmail}
        />
      )}

      {/* Delete Confirmation Modal */}
      {selectedCandidateForDelete && (
        <DeleteConfirmModal
          isOpen={Boolean(selectedCandidateForDelete)}
          onClose={() => setSelectedCandidateForDelete(null)}
          onConfirm={handleDeleteCandidate}
          title="Delete Candidate Record"
          message={`Are you sure you want to delete ${selectedCandidateForDelete.first_name} ${selectedCandidateForDelete.last_name}? This action cannot be undone.`}
          isLoading={deleting}
        />
      )}
    </div>
  );
};

export default CandidateList;
