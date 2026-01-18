import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Activity, GitBranch, FileText } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { path: '/', label: 'Overview', icon: LayoutDashboard },
    { path: '/drift', label: 'Drift Analysis', icon: Activity },
    { path: '/retraining', label: 'Retraining', icon: GitBranch },
    { path: '/reports', label: 'Reports', icon: FileText },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen fixed left-0 top-0 border-r border-slate-800">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold text-white tracking-tight">ML Monitor</h1>
        <p className="text-xs text-slate-500 mt-1">Platform Operations</p>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${isActive
                ? 'bg-indigo-600 text-white shadow-sm'
                : 'hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <item.icon size={18} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center gap-3 px-2">
          <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white font-bold text-xs">
            OP
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">Platform Ops</p>
            <p className="text-xs text-slate-500 truncate">admin@platform.co</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
