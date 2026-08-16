import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Candidate } from '../../types';
import Badge from '../common/Badge';
import { User, Mail, Phone, Calendar, Pencil, Trash2 } from 'lucide-react';

interface CandidateCardProps {
  candidate: Candidate;
  onEdit?: (candidate: Candidate) => void;
  onDelete?: (candidate: Candidate) => void;
}

const CandidateCard: React.FC<CandidateCardProps> = ({ candidate, onEdit, onDelete }) => {
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

  const formattedDate = new Date(candidate.created_at).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <div
      onClick={() => navigate(`/candidates/${candidate.id}`)}
      className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex flex-col justify-between font-sans transition hover:shadow-md cursor-pointer h-full"
    >
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="w-10 h-10 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center border border-slate-200">
            <User size={18} />
          </div>
          <div className="flex items-center gap-1.5">
            <Badge variant={getStatusVariant(candidate.status)}>{candidate.status}</Badge>
            {onEdit && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onEdit(candidate);
                }}
                className="text-slate-400 hover:text-brand-600 p-1 rounded-md transition"
                title="Edit Details"
              >
                <Pencil size={14} />
              </button>
            )}
            {onDelete && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onDelete(candidate);
                }}
                className="text-slate-400 hover:text-red-600 p-1 rounded-md transition"
                title="Delete Candidate"
              >
                <Trash2 size={14} />
              </button>
            )}
          </div>
        </div>

        <h3 className="text-[14px] font-bold text-slate-800 tracking-tight leading-tight">
          {candidate.first_name} {candidate.last_name}
        </h3>

        <div className="space-y-1.5 mt-4">
          <div className="flex items-center gap-2 text-slate-400">
            <Mail size={13} className="shrink-0" />
            <span className="text-[11px] font-medium text-slate-500 line-clamp-1">{candidate.email}</span>
          </div>
          {candidate.phone && (
            <div className="flex items-center gap-2 text-slate-400">
              <Phone size={13} className="shrink-0" />
              <span className="text-[11px] font-medium text-slate-500">{candidate.phone}</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-slate-400">
            <Calendar size={13} className="shrink-0" />
            <span className="text-[11px] font-medium text-slate-400">Applied {formattedDate}</span>
          </div>
        </div>
      </div>

      {/* Skills list tags */}
      {candidate.candidate_skills && candidate.candidate_skills.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-5 pt-4 border-t border-slate-50">
          {candidate.candidate_skills.slice(0, 3).map((cs) => (
            <Badge key={cs.skill.id} variant="slate" className="px-2 py-0">
              {cs.skill.name}
            </Badge>
          ))}
          {candidate.candidate_skills.length > 3 && (
            <span className="text-[10px] text-slate-400 font-bold self-center">
              +{candidate.candidate_skills.length - 3} more
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default CandidateCard;
