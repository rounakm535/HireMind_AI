import React from 'react';

interface LoaderProps {
  size?: 'xs' | 'sm' | 'md' | 'lg';
  className?: string;
}

const Loader: React.FC<LoaderProps> = ({ size = 'md', className = '' }) => {
  const sizes = {
    xs: 'w-3 h-3 border-2',
    sm: 'w-5 h-5 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4',
  };

  return (
    <div
      className={`animate-spin rounded-full border-solid border-slate-200 border-t-current ${sizes[size]} ${className}`}
      style={{ borderTopColor: 'currentColor' }}
      role="status"
    />
  );
};

export default Loader;
