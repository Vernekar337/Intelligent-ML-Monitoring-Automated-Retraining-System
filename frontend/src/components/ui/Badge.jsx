import React from 'react';

const Badge = ({ status, className = '' }) => {
  const getStyles = () => {
    switch (status?.toLowerCase()) {
      case 'healthy':
      case 'ok':
      case 'success':
        return 'bg-green-50 text-green-700 ring-1 ring-inset ring-green-600/20';
      case 'warning':
        return 'bg-yellow-50 text-yellow-800 ring-1 ring-inset ring-yellow-600/20';
      case 'critical':
      case 'error':
      case 'failure':
        return 'bg-red-50 text-red-700 ring-1 ring-inset ring-red-600/10';
      default:
        return 'bg-gray-50 text-gray-600 ring-1 ring-inset ring-gray-500/10';
    }
  };

  return (
    <span
      className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${getStyles()} ${className}`}
    >
      {status?.toUpperCase() || 'UNKNOWN'}
    </span>
  );
};

export default Badge;
