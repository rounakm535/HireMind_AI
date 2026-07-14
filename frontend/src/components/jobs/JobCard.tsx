import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Job } from '../../types';
import Badge from '../common/Badge';
import { Briefcase, MapPin, Edit3, Trash2 } from 'lucide-react';
import Button from '../common/Button';

interface JobCardProps {
  job: Job;
  onDelete?: (id: string) => void;
}

const JobCard: React.FC<JobCardProps> = ({ job, onDelete }) => {
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

  const getJobTypeLabel = (type: string) => {
    return type.replace('_', ' ');
  };

  return (
    <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex flex-col justify-between font-sans transition hover:shadow-md h-full">
      {/* Card Top */}
      <div>
        <div className="flex items-center justify-between gap-3 mb-3">
          <Badge variant={getStatusVariant(job.status)}>{job.status}</Badge>
          <span className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
            {getJobTypeLabel(job.job_type)}
          </span>
        </div>
        <h3 className="text-[15px] font-bold text-slate-800 tracking-tight leading-snug line-clamp-1">
          {job.title}
        </h3>
        <div className="flex items-center gap-1.5 text-slate-400 mt-2">
          <MapPin size={14} className="shrink-0" />
          <span className="text-[11px] font-medium">{job.location}</span>
        </div>
        <p className="text-[12px] text-slate-500 line-clamp-3 mt-3.5 leading-relaxed font-medium">
          {job.description}
        </p>
      </div>

      {/* Card Footer Actions */}
      <div className="flex items-center justify-between border-t border-slate-50 mt-5 pt-4">
        <Button
          variant="outline"
          size="sm"
          onClick={() => navigate(`/jobs/${job.id}`)}
          className="gap-1.5"
        >
          <Edit3 size={13} />
          <span>Edit</span>
        </Button>

        {onDelete && (
          <button
            onClick={() => onDelete(job.id)}
            className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
          >
            <Trash2 size={15} />
          </button>
        )}
      </div>
    </div>
  );
};

export default JobCard;
