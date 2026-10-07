import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Candidate } from '../../types';
import Table, { TableColumn } from '../common/Table';
import Badge from '../common/Badge';
import { Calendar, ChevronRight, Pencil, Trash2, Mail, Sparkles } from 'lucide-react';

interface CandidateTableProps {
  candidates: Candidate[];
  isLoading?: boolean;
  onEdit?: (candidate: Candidate) => void;
  onDelete?: (candidate: Candidate) => void;
  onSendEmail?: (candidate: Candidate) => void;
}

const CandidateTable: React.FC<CandidateTableProps> = ({
  candidates,
  isLoading = false,
  onEdit,
  onDelete,
  onSendEmail,
}) => {
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

  const columns: TableColumn<Candidate>[] = [
    {
      key: 'name',
      header: 'Candidate Name',
      render: (candidate) => (
        <span
          className="font-bold text-slate-800 hover:text-brand-600 cursor-pointer text-xs"
          onClick={() => navigate(`/candidates/${candidate.id}`)}
        >
          {candidate.first_name} {candidate.last_name}
        </span>
      ),
    },
    {
      key: 'email',
      header: 'Email Address',
      render: (candidate) => <span className="text-xs text-slate-600">{candidate.email}</span>,
    },
    {
      key: 'match_score',
      header: 'AI Match Score',
      render: (candidate) => {
        const score =
          candidate.match_scores && candidate.match_scores.length > 0
            ? Math.round(candidate.match_scores[0].score)
            : null;

        if (score === null) {
          return <span className="text-[11px] font-semibold text-slate-400">Not Screened</span>;
        }

        return (
          <span
            className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${
              score >= 80
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : score >= 60
                ? 'bg-brand-50 text-brand-700 border-brand-200'
                : 'bg-amber-50 text-amber-700 border-amber-200'
            }`}
          >
            <Sparkles size={11} className={score >= 80 ? 'text-emerald-500 fill-emerald-500' : 'text-brand-500 fill-brand-500'} />
            <span>{score}%</span>
          </span>
        );
      },
    },
    {
      key: 'status',
      header: 'Status',
      render: (candidate) => <Badge variant={getStatusVariant(candidate.status)}>{candidate.status}</Badge>,
    },
    {
      key: 'created_at',
      header: 'Applied Date',
      render: (candidate) => {
        const date = new Date(candidate.created_at).toLocaleDateString(undefined, {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
        });
        return (
          <span className="flex items-center gap-1.5 text-slate-400 text-xs">
            <Calendar size={13} />
            <span>{date}</span>
          </span>
        );
      },
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (candidate) => (
        <div className="flex items-center gap-1 justify-end">
          {onSendEmail && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onSendEmail(candidate);
              }}
              className="text-slate-400 hover:text-brand-600 hover:bg-brand-50 p-1.5 rounded-lg transition"
              title="Send Email Directly"
            >
              <Mail size={15} />
            </button>
          )}
          {onEdit && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onEdit(candidate);
              }}
              className="text-slate-400 hover:text-brand-600 hover:bg-slate-50 p-1.5 rounded-lg transition"
              title="Edit Candidate"
            >
              <Pencil size={15} />
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
              <Trash2 size={15} />
            </button>
          )}
          <button
            onClick={() => navigate(`/candidates/${candidate.id}`)}
            className="text-slate-400 hover:text-brand-600 hover:bg-slate-50 transition p-1.5 rounded-lg"
            title="View Details"
          >
            <ChevronRight size={16} />
          </button>
        </div>
      ),
    },
  ];

  return <Table columns={columns} data={candidates} isLoading={isLoading} emptyMessage="No candidates found." />;
};

export default CandidateTable;
