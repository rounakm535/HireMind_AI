import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Candidate } from '../../types';
import Badge from '../common/Badge';

interface RecentCandidatesProps {
  candidates: Candidate[];
}

const RecentCandidates: React.FC<RecentCandidatesProps> = ({ candidates }) => {
  const navigate = useNavigate();

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'NEW':
        return 'brand';
      case 'SCREENING':
        return 'info';
      case 'INTERVIEWING':
        return 'warning';
      case 'OFFERED':
      case 'HIRED':
        return 'success';
      case 'REJECTED':
        return 'danger';
      default:
        return 'slate';
    }
  };

  return (
    <div className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden font-sans">
      <div className="px-6 py-4 border-b border-slate-50 flex items-center justify-between">
        <h2 className="text-[14px] font-bold text-slate-800 tracking-tight">Recent Candidates</h2>
        <button
          onClick={() => navigate('/candidates')}
          className="text-[12px] font-semibold text-brand-600 hover:text-brand-700"
        >
          View All
        </button>
      </div>

      <div className="divide-y divide-slate-50">
        {candidates.length === 0 ? (
          <div className="p-6 text-center text-[12px] text-slate-400">No candidate profile registered.</div>
        ) : (
          candidates.slice(0, 5).map((candidate) => (
            <div
              key={candidate.id}
              onClick={() => navigate(`/candidates/${candidate.id}`)}
              className="px-6 py-3.5 flex items-center justify-between hover:bg-slate-50/50 cursor-pointer transition"
            >
              <div>
                <p className="text-[13px] font-semibold text-slate-700">
                  {candidate.first_name} {candidate.last_name}
                </p>
                <p className="text-[11px] text-slate-400 mt-0.5">{candidate.email}</p>
              </div>
              <Badge variant={getStatusVariant(candidate.status)}>{candidate.status}</Badge>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default RecentCandidates;
