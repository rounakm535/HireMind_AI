import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Candidate } from '../../types';
import Badge from '../common/Badge';
import { User, Mail, Phone, Calendar, Pencil, Trash2, Sparkles, Send } from 'lucide-react';

interface CandidateCardProps {
  candidate: Candidate;
  onEdit?: (candidate: Candidate) => void;
  onDelete?: (candidate: Candidate) => void;
  onSendEmail?: (candidate: Candidate) => void;
}

const CandidateCard: React.FC<CandidateCardProps> = ({ candidate, onEdit, onDelete, onSendEmail }) => {
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

  // Calculate Match Score
  const matchScore =
    candidate.match_scores && candidate.match_scores.length > 0
      ? Math.round(candidate.match_scores[0].score)
      : null;

  return (
    <div
      onClick={() => navigate(`/candidates/${candidate.id}`)}
      className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex flex-col justify-between font-sans transition hover:shadow-md hover:border-slate-200 cursor-pointer h-full group"
    >
      <div>
        {/* Card Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="w-10 h-10 rounded-full bg-slate-100 text-slate-500 flex items-center justify-center border border-slate-200 font-bold text-xs uppercase">
            {candidate.first_name?.[0] && candidate.last_name?.[0]
              ? `${candidate.first_name[0]}${candidate.last_name[0]}`
              : <User size={18} />}
          </div>

          <div className="flex items-center gap-1.5">
            <Badge variant={getStatusVariant(candidate.status)}>{candidate.status}</Badge>

            {onSendEmail && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onSendEmail(candidate);
                }}
                className="text-slate-400 hover:text-brand-600 hover:bg-brand-50 p-1.5 rounded-lg transition"
                title="Send Email Directly"
              >
                <Mail size={14} />
              </button>
            )}

            {onEdit && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onEdit(candidate);
                }}
                className="text-slate-400 hover:text-brand-600 hover:bg-slate-50 p-1.5 rounded-lg transition"
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
                className="text-slate-400 hover:text-red-600 hover:bg-red-50 p-1.5 rounded-lg transition"
                title="Delete Candidate"
              >
                <Trash2 size={14} />
              </button>
            )}
          </div>
        </div>

        {/* Candidate Name & Match Percentage Row */}
        <div className="flex items-start justify-between gap-2">
          <h3 className="text-[15px] font-bold text-slate-800 tracking-tight leading-tight group-hover:text-brand-600 transition">
            {candidate.first_name} {candidate.last_name}
          </h3>

          {/* Match Score Badge */}
          {matchScore !== null ? (
            <div
              className={`shrink-0 inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-black tracking-tight border ${
                matchScore >= 80
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : matchScore >= 60
                  ? 'bg-brand-50 text-brand-700 border-brand-200'
                  : 'bg-amber-50 text-amber-700 border-amber-200'
              }`}
              title="AI Screened Match Percentage"
            >
              <Sparkles size={11} className={matchScore >= 80 ? 'text-emerald-500 fill-emerald-500' : 'text-brand-500 fill-brand-500'} />
              <span>{matchScore}% Match</span>
            </div>
          ) : (
            <div className="shrink-0 inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold text-slate-400 bg-slate-50 border border-slate-200">
              Not Screened
            </div>
          )}
        </div>

        {/* Candidate Contact Meta */}
        <div className="space-y-1.5 mt-4">
          <div className="flex items-center gap-2 text-slate-400">
            <Mail size={13} className="shrink-0 text-slate-400" />
            <span className="text-[12px] font-medium text-slate-600 line-clamp-1">{candidate.email}</span>
          </div>
          {candidate.phone && (
            <div className="flex items-center gap-2 text-slate-400">
              <Phone size={13} className="shrink-0 text-slate-400" />
              <span className="text-[12px] font-medium text-slate-600">{candidate.phone}</span>
            </div>
          )}
          <div className="flex items-center gap-2 text-slate-400">
            <Calendar size={13} className="shrink-0 text-slate-400" />
            <span className="text-[11px] font-medium text-slate-400">Applied {formattedDate}</span>
          </div>
        </div>
      </div>

      {/* Skills & Action Footer */}
      <div className="mt-5 pt-4 border-t border-slate-100 flex flex-col gap-3">
        {/* Skills list tags */}
        {candidate.candidate_skills && candidate.candidate_skills.length > 0 ? (
          <div className="flex flex-wrap gap-1.5 items-center">
            {candidate.candidate_skills.slice(0, 3).map((cs) => (
              <Badge key={cs.skill.id} variant="slate" className="px-2 py-0.5 text-[10px]">
                {cs.skill.name}
              </Badge>
            ))}
            {candidate.candidate_skills.length > 3 && (
              <span className="text-[10px] text-slate-400 font-bold self-center">
                +{candidate.candidate_skills.length - 3} more
              </span>
            )}
          </div>
        ) : (
          <span className="text-[11px] text-slate-400 italic">No skills tagged</span>
        )}

        {/* Direct Action Buttons */}
        <div className="flex items-center justify-between pt-1">
          <button
            onClick={(e) => {
              e.stopPropagation();
              onSendEmail?.(candidate);
            }}
            className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 hover:text-brand-700 bg-brand-50 hover:bg-brand-100/80 px-3 py-1.5 rounded-lg transition"
          >
            <Send size={12} />
            <span>Send Email</span>
          </button>

          <span className="text-xs font-semibold text-slate-400 hover:text-slate-600">
            View Details &rarr;
          </span>
        </div>
      </div>
    </div>
  );
};

export default CandidateCard;
