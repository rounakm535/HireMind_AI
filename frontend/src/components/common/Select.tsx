import React, { forwardRef, SelectHTMLAttributes } from 'react';

interface SelectOption {
  value: string;
  label: string;
}

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: SelectOption[];
  error?: string;
  className?: string;
}

const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, options, error, className = '', id, ...props }, ref) => {
    return (
      <div className="flex flex-col gap-1.5 w-full font-sans">
        {label && (
          <label htmlFor={id} className="text-[13px] font-semibold text-slate-700">
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={id}
          className={`w-full text-[13px] text-slate-800 border px-3.5 py-2 rounded-lg bg-white focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 transition ${
            error ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'border-slate-200'
          } ${className}`}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <span className="text-[11px] font-semibold text-red-500 mt-0.5">{error}</span>}
      </div>
    );
  }
);

Select.displayName = 'Select';

export default Select;
