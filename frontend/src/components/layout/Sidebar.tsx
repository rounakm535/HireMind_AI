import React from 'react';
import { NavLink } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { logout } from '../../redux/slices/authSlice';
import {
  LayoutDashboard,
  Briefcase,
  Users,
  UploadCloud,
  MessageSquare,
  Mail,
  BarChart2,
  LogOut,
  Sparkles,
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const dispatch = useDispatch();

  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/jobs', label: 'Jobs', icon: Briefcase },
    { to: '/candidates', label: 'Candidates', icon: Users },
    { to: '/resume/upload', label: 'Upload Resume', icon: UploadCloud },
    { to: '/chat', label: 'AI Chatbot', icon: MessageSquare },
    { to: '/emails', label: 'Generate Email', icon: Mail },
    { to: '/analytics', label: 'Analytics', icon: BarChart2 },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-100 flex flex-col h-screen font-sans">
      {/* Brand Header */}
      <div className="h-16 flex items-center px-6 border-b border-slate-50 gap-2.5">
        <div className="bg-brand-500 text-white p-1.5 rounded-lg flex items-center justify-center">
          <Sparkles size={20} className="fill-white/10" />
        </div>
        <span className="text-lg font-bold text-brand-900 tracking-tight">HireMind AI</span>
      </div>

      {/* Nav Links */}
      <nav className="flex-1 py-6 px-4 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-2.5 rounded-xl text-[14px] font-medium transition ${
                isActive
                  ? 'bg-brand-50 text-brand-600 shadow-sm shadow-brand-100/10'
                  : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
              }`
            }
          >
            <item.icon size={18} className="shrink-0" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Bottom Profile / Logout */}
      <div className="p-4 border-t border-slate-50">
        <button
          onClick={() => dispatch(logout())}
          className="flex w-full items-center gap-3 px-4 py-2.5 rounded-xl text-[14px] font-medium text-red-500 hover:bg-red-50 hover:text-red-600 transition"
        >
          <LogOut size={18} className="shrink-0" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
