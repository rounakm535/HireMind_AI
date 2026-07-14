import React, { useState } from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';
import Button from './Button';

interface SearchBarProps {
  placeholder?: string;
  onSearch: (query: string) => void;
  showFiltersToggle?: boolean;
  onFiltersToggle?: () => void;
}

const SearchBar: React.FC<SearchBarProps> = ({
  placeholder = 'Search...',
  onSearch,
  showFiltersToggle = false,
  onFiltersToggle,
}) => {
  const [value, setValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(value);
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-center gap-3 w-full max-w-xl font-sans">
      <div className="relative flex-1">
        <span className="absolute inset-y-0 left-0 flex items-center pl-3.5 pointer-events-none text-slate-400">
          <Search size={16} />
        </span>
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder={placeholder}
          className="w-full text-[13px] border border-slate-200 bg-white rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-1 focus:ring-brand-500 focus:border-brand-500 transition"
        />
      </div>
      <Button type="submit" variant="primary" size="md" className="py-2.5">
        Search
      </Button>
      {showFiltersToggle && onFiltersToggle && (
        <Button
          type="button"
          variant="outline"
          size="md"
          onClick={onFiltersToggle}
          className="px-3"
        >
          <SlidersHorizontal size={16} />
        </Button>
      )}
    </form>
  );
};

export default SearchBar;
