import React from 'react';
import { LucideIcon } from 'lucide-react';
import Button from './Button';

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  onActionClick?: () => void;
}

const EmptyState: React.FC<EmptyStateProps> = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onActionClick,
}) => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 bg-white border border-slate-100 rounded-2xl shadow-sm font-sans max-w-lg mx-auto my-12">
      <div className="bg-brand-50 text-brand-500 p-4 rounded-full mb-4">
        <Icon size={28} />
      </div>
      <h3 className="text-[15px] font-bold text-slate-800 tracking-tight mb-1">{title}</h3>
      <p className="text-[13px] text-slate-500 max-w-sm mb-6 leading-normal font-medium">
        {description}
      </p>
      {actionLabel && onActionClick && (
        <Button variant="primary" size="md" onClick={onActionClick}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};

export default EmptyState;
