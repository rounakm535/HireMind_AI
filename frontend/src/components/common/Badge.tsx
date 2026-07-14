import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'brand' | 'success' | 'warning' | 'danger' | 'info' | 'slate';
  className?: string;
}

const Badge: React.FC<BadgeProps> = ({ children, variant = 'slate', className = '' }) => {
  const variants = {
    brand: 'bg-brand-50 text-brand-600 border border-brand-100',
    success: 'bg-green-50 text-green-700 border border-green-100',
    warning: 'bg-yellow-50 text-yellow-700 border border-yellow-100',
    danger: 'bg-red-50 text-red-700 border border-red-100',
    info: 'bg-blue-50 text-blue-700 border border-blue-100',
    slate: 'bg-slate-50 text-slate-600 border border-slate-100',
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold tracking-wide ${variants[variant]} ${className}`}
    >
      {children}
    </span>
  );
};

export default Badge;
