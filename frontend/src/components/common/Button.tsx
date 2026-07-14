import React, { ButtonHTMLAttributes } from 'react';
import Loader from './Loader';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className = '',
  disabled,
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-brand-600 text-white hover:bg-brand-700 focus:ring-brand-500 shadow-sm border border-transparent',
    secondary: 'bg-slate-100 text-slate-700 hover:bg-slate-200 focus:ring-slate-400 border border-transparent',
    outline: 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 focus:ring-slate-400',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500 shadow-sm border border-transparent',
    ghost: 'bg-transparent text-slate-500 hover:bg-slate-50 hover:text-slate-700 focus:ring-slate-400 border border-transparent',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-[13px]',
    lg: 'px-5 py-2.5 text-[15px]',
  };

  const stateStyles = (disabled || isLoading) ? 'opacity-65 cursor-not-allowed' : '';

  return (
    <button
      disabled={disabled || isLoading}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${stateStyles} ${className}`}
      {...props}
    >
      {isLoading && <Loader size="xs" className="mr-2 text-current" />}
      {children}
    </button>
  );
};

export default Button;
