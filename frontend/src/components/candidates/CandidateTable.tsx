import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Candidate } from '../../types';
import Table, { TableColumn } from '../common/Table';
import Badge from '../common/Badge';
import { Calendar, ChevronRight } from 'lucide-react';

interface CandidateTableProps {
  candidates: Candidate[];
  isLoading?: boolean;
}

const CandidateTable: React.FC<CandidateTableProps> = ({ candidates, isLoading = false }) => {
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
      header: '',
      render: (candidate) => (
        <button
          onClick={() => navigate(`/candidates/${candidate.id}`)}
          className="text-slate-400 hover:text-brand-600 transition p-1"
        >
          <ChevronRight size={16} />
        </button>
      ),
    },
  ];

  return <Table columns={columns} data={candidates} isLoading={isLoading} emptyMessage="No candidates found." />;
};

export default CandidateTable;
