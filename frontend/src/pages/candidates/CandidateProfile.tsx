import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { fetchCandidateDetails, screenAndMatchResume, clearCurrentCandidate, deleteCandidateProfile } from '../../redux/slices/candidateSlice';
import { fetchJobs } from '../../redux/slices/jobSlice';
import PageHeader from '../../components/layout/PageHeader';
import CandidateDetails from '../../components/candidates/CandidateDetails';
import ResumeViewer from '../../components/candidates/ResumeViewer';
import Loader from '../../components/common/Loader';
import Select from '../../components/common/Select';
import Button from '../../components/common/Button';
import EditCandidateModal from '../../components/candidates/EditCandidateModal';
import DeleteConfirmModal from '../../components/common/DeleteConfirmModal';
import { ArrowLeft, Play, Sparkles, Pencil, Trash2 } from 'lucide-react';

const CandidateProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  // Redux Selectors
  const { currentCandidate, currentMatch, loading, actionLoading } = useAppSelector((state) => state.candidates);
  const { jobs } = useAppSelector((state) => state.jobs);

  // States
  const [selectedJobId, setSelectedJobId] = useState<string>('');
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    if (id) {
      dispatch(fetchCandidateDetails(id));
      dispatch(fetchJobs({ status: 'OPEN' })); // Get open positions for matching
    }
    return () => {
      dispatch(clearCurrentCandidate());
    };
  }, [id, dispatch]);

  const handleScreen = async () => {
    if (!id || !selectedJobId || !currentCandidate) return;
    
    // Find candidate's resume (use first resume found, since upload_resume saves it)
    const resumeId = currentCandidate.resumes?.[0]?.id;
    if (!resumeId) {
      alert('This candidate has no uploaded resume to parse. Please upload a resume first.');
      return;
    }

    const res = await dispatch(screenAndMatchResume({ resumeId, jobId: selectedJobId }));
    if (screenAndMatchResume.fulfilled.match(res)) {
      dispatch(fetchCandidateDetails(id));
    }
  };

  const handleDeleteCandidate = async () => {
    if (!id) return;
    setDeleting(true);
    const res = await dispatch(deleteCandidateProfile(id));
    if (deleteCandidateProfile.fulfilled.match(res)) {
      navigate('/candidates');
    }
    setDeleting(false);
  };

  if (loading && !currentCandidate) {
    return (
      <div className="h-[50vh] w-full flex items-center justify-center">
        <Loader size="lg" className="text-brand-500" />
      </div>
    );
  }

  if (!currentCandidate) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-400 text-sm">Candidate profile not found.</p>
        <Button variant="primary" size="sm" onClick={() => navigate('/candidates')} className="mt-4">
          Back to list
        </Button>
      </div>
    );
  }

  const jobOptions = [
    { value: '', label: 'Select job post to match...' },
    ...jobs.map((j) => ({ value: j.id, label: j.title })),
  ];

  const candidateResume = currentCandidate.resumes?.[0];

  return (
    <div className="font-sans space-y-6">
      {/* Header */}
      <PageHeader title="Candidate Profile" subtitle="Detailed information and AI match parameters evaluation.">
        <div className="flex flex-wrap items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => setIsEditModalOpen(true)} className="gap-1.5 h-9">
            <Pencil size={15} />
            <span>Edit Details</span>
          </Button>
          <Button variant="danger" size="sm" onClick={() => setIsDeleteModalOpen(true)} className="gap-1.5 h-9">
            <Trash2 size={15} />
            <span>Delete Candidate</span>
          </Button>
          <Button variant="outline" size="sm" onClick={() => navigate('/candidates')} className="gap-1.5 h-9">
            <ArrowLeft size={16} />
            <span>Back to List</span>
          </Button>
        </div>
      </PageHeader>

      {/* Quick AI screening controller Action Panel */}
      <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="bg-brand-50 text-brand-500 p-2 rounded-lg">
            <Sparkles size={18} />
          </div>
          <div>
            <h4 className="text-[13px] font-bold text-slate-800">Match against Open Roles</h4>
            <p className="text-[11px] text-slate-400 mt-0.5">Select a position and trigger the AI screening engine.</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="w-64">
            <Select
              options={jobOptions}
              value={selectedJobId}
              onChange={(e) => setSelectedJobId(e.target.value)}
            />
          </div>
          <Button
            variant="primary"
            size="md"
            disabled={!selectedJobId || actionLoading}
            onClick={handleScreen}
            className="gap-1.5 py-2.5"
            isLoading={actionLoading}
          >
            <Play size={14} className="fill-current" />
            <span>Run AI screening</span>
          </Button>
        </div>
      </div>

      {/* Split Grid Profile Layout */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
        {/* Left Side: Candidate details sheet */}
        <CandidateDetails
          candidate={currentCandidate}
          matchScore={currentMatch || currentCandidate.match_scores?.[0]}
          questions={candidateResume?.interview_questions}
        />

        {/* Right Side: Resume Reader Document preview */}
        {candidateResume ? (
          <ResumeViewer resume={candidateResume} />
        ) : (
          <div className="bg-white border border-slate-100 rounded-2xl p-12 text-center text-slate-400 flex flex-col items-center justify-center h-64 shadow-sm">
            <p className="text-xs font-semibold mb-3">No resume document uploaded for this applicant.</p>
            <Button variant="outline" size="sm" onClick={() => navigate('/resume/upload')} className="py-2.5">
              Upload Resume Now
            </Button>
          </div>
        )}
      </div>

      {/* Edit Modal */}
      {isEditModalOpen && (
        <EditCandidateModal
          isOpen={isEditModalOpen}
          onClose={() => setIsEditModalOpen(false)}
          candidate={currentCandidate}
          onSuccess={() => {
            if (id) dispatch(fetchCandidateDetails(id));
          }}
        />
      )}

      {/* Delete Confirmation Modal */}
      {isDeleteModalOpen && (
        <DeleteConfirmModal
          isOpen={isDeleteModalOpen}
          onClose={() => setIsDeleteModalOpen(false)}
          onConfirm={handleDeleteCandidate}
          title="Delete Candidate Record"
          message={`Are you sure you want to delete ${currentCandidate.first_name} ${currentCandidate.last_name}? All associated resumes, match scores, and interview questions will be permanently removed.`}
          isLoading={deleting}
        />
      )}
    </div>
  );
};

export default CandidateProfile;
