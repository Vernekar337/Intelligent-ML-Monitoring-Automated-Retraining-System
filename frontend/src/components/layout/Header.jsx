import React from 'react';

const Header = () => {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <h2 className="text-lg font-semibold text-gray-800">Dashboard</h2>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-500">Production Environment</span>
        <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
      </div>
    </header>
  );
};

export default Header;
