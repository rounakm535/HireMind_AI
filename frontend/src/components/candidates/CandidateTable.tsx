import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Candidate } from '../../types';
import Table, { TableColumn } from '../common/Table';
import Badge from '../common/Badge';
import { Calendar, ChevronRight, Pencil, Trash2 } from 'lucide-react';

interface CandidateTableProps {
  candidates: Candidate[];
  isLoading?: boolean;
  onEdit?: (candidate: Candidate) => void;
  onDelete?: (candidate: Candidate) => void;
}

const CandidateTable: React.FC<CandidateTableProps> = ({ candidates, isLoading = false, onEdit, onDelete }) => {
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
          className="font-semibold text-slate-800 hover:text-brand-600 cursor-pointer"
          onClick={() => navigate(`/candidates/${candidate.id}`)}
        >
          {candidate.first_name} {candidate.last_name}
        </span>
      ),
    },
    {
      key: 'email',
      header: 'Email Address',
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
          <span className="flex items-center gap-1.5 text-slate-400">
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
          {onEdit && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onEdit(candidate);
              }}
              className="text-slate-400 hover:text-brand-600 p-1.5 rounded-lg transition"
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
              className="text-slate-400 hover:text-red-600 p-1.5 rounded-lg transition"
              title="Delete Candidate"
            >
              <Trash2 size={15} />
            </button>
          )}
          <button
            onClick={() => navigate(`/candidates/${candidate.id}`)}
            className="text-slate-400 hover:text-brand-600 transition p-1.5 rounded-lg"
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
