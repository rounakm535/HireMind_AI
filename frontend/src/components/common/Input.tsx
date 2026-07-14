import React, { forwardRef, InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  className?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className = '', type = 'text', id, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5 w-full font-sans">
        {label && (
          <label htmlFor={id} className="text-[13px] font-semibold text-slate-700">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={id}
          type={type}
          className={`w-full text-[13px] text-slate-800 border px-3.5 py-2 rounded-lg bg-white placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 transition ${
            error ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-slate-200'
          } ${className}`}
          {...props}
        />
        {error && <span className="text-[11px] font-semibold text-red-500 mt-0.5">{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
