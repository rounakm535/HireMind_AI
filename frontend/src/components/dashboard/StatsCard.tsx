import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  color?: 'brand' | 'success' | 'warning' | 'info';
  description?: string;
}

const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  icon: Icon,
  color = 'brand',
  description,
}) => {
  const bgColors = {
    brand: 'bg-brand-50 text-brand-500 border-brand-100',
    success: 'bg-green-50 text-green-600 border-green-100',
    warning: 'bg-yellow-50 text-yellow-600 border-yellow-100',
    info: 'bg-blue-50 text-blue-600 border-blue-100',
  };

  return (
    <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex items-center gap-5 font-sans transition hover:shadow-md">
      <div className={`p-4 rounded-xl border ${bgColors[color]} flex items-center justify-center shrink-0`}>
        <Icon size={24} />
      </div>
      <div>
        <h3 className="text-[12px] font-bold text-slate-400 uppercase tracking-wider">{title}</h3>
        <p className="text-2xl font-bold text-slate-800 leading-none mt-1.5">{value}</p>
        {description && <p className="text-[11px] text-slate-400 mt-1 font-medium">{description}</p>}
      </div>
    </div>
  );
};

export default StatsCard;
