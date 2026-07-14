import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Job } from '../../types';
import Table, { TableColumn } from '../common/Table';
import Badge from '../common/Badge';
import Button from '../common/Button';
import { Edit3, Trash2 } from 'lucide-react';

interface JobTableProps {
  jobs: Job[];
  isLoading?: boolean;
  onDelete?: (id: string) => void;
}

const JobTable: React.FC<JobTableProps> = ({ jobs, isLoading = false, onDelete }) => {
  const navigate = useNavigate();

  const getStatusVariant = (status: string) => {
    switch (status) {
      case 'OPEN':
        return 'success';
      case 'CLOSED':
        return 'danger';
      case 'DRAFT':
        return 'slate';
      default:
        return 'info';
    }
  };

  const columns: TableColumn<Job>[] = [
    {
      key: 'title',
      header: 'Job Title',
      render: (job) => (
        <span className="font-semibold text-slate-800 hover:text-brand-600 cursor-pointer" onClick={() => navigate(`/jobs/${job.id}`)}>
          {job.title}
        </span>
      ),
    },
    {
      key: 'job_type',
      header: 'Type',
      render: (job) => <span className="capitalize">{job.job_type.toLowerCase().replace('_', ' ')}</span>,
    },
    {
      key: 'location',
      header: 'Location',
    },
    {
      key: 'status',
      header: 'Status',
      render: (job) => <Badge variant={getStatusVariant(job.status)}>{job.status}</Badge>,
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (job) => (
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" onClick={() => navigate(`/jobs/${job.id}`)} className="p-1">
            <Edit3 size={14} className="text-slate-500 hover:text-brand-600" />
          </Button>
          {onDelete && (
            <Button variant="ghost" size="sm" onClick={() => onDelete(job.id)} className="p-1">
              <Trash2 size={14} className="text-red-400 hover:text-red-600" />
            </Button>
          )}
        </div>
      ),
    },
  ];

  return <Table columns={columns} data={jobs} isLoading={isLoading} emptyMessage="No jobs found." />;
};

export default JobTable;
