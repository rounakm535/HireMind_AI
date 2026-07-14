import React from 'react';
import { useSelector } from 'react-redux';
import { RootState } from '../../app/store';
import { Bell, Search, ShieldCheck } from 'lucide-react';

const Topbar: React.FC = () => {
  const { user } = useSelector((state: RootState) => state.auth);

  return (
    <header className="h-16 bg-white border-b border-slate-100 flex items-center justify-between px-8 font-sans shrink-0">
      {/* Search Input Box */}
      <div className="relative w-80">
        <span className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-slate-400">
          <Search size={16} />
        </span>
        <input
          type="text"
          placeholder="Global search candidates..."
          className="w-full text-[13px] bg-slate-50 border border-transparent rounded-lg pl-10 pr-4 py-1.5 focus:bg-white focus:border-brand-200 focus:outline-none transition"
        />
      </div>

      {/* Notifications, User Profile info */}
      <div className="flex items-center gap-6">
        {/* Notifications Icon */}
        <button className="text-slate-400 hover:text-slate-600 relative">
          <Bell size={18} />
          <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full ring-2 ring-white"></span>
        </button>

        {/* Vertical Separator */}
        <span className="h-6 w-px bg-slate-100"></span>

        {/* User Card */}
        {user && (
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-[13px] font-semibold text-slate-800 leading-tight">
                {user.first_name} {user.last_name}
              </p>
              <div className="flex items-center justify-end gap-1.5 mt-0.5">
                <ShieldCheck size={12} className="text-brand-500" />
                <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                  {user.role.replace('_', ' ')}
                </span>
              </div>
            </div>
            
            {/* User Avatar Initials */}
            <div className="w-9 h-9 rounded-full bg-brand-100 text-brand-700 font-bold text-xs flex items-center justify-center border border-brand-200">
              {user.first_name[0]}
              {user.last_name[0]}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Topbar;
