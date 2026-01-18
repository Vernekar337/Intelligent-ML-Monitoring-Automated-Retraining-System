import React from 'react';

const HistoryChart = ({ data, metric, color = 'indigo' }) => {
  if (!data || data.length === 0) return null;

  const values = data.map(d => d[metric]);
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  // SVG Dimensions
  const height = 100;
  const width = 300;

  // Transform data points to SVG coordinates
  const points = values.map((val, index) => {
    const x = (index / (values.length - 1)) * width;
    const padding = 10; // Padding to avoid clipping top/bottom
    const availableHeight = height - (padding * 2);
    // Invert Y because SVG 0 is top
    const y = height - padding - (((val - min) / range) * availableHeight);
    return `${x},${y}`;
  }).join(' ');

  const strokeColor = {
    indigo: 'stroke-indigo-600',
    green: 'stroke-green-600',
    blue: 'stroke-blue-600',
  }[color] || 'stroke-indigo-600';

  return (
    <div className="w-full h-full flex items-center justify-center">
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-full overflow-visible">
        {/* Grid lines */}
        <line x1="0" y1={height} x2={width} y2={height} className="stroke-gray-200" strokeWidth="1" />
        <line x1="0" y1="0" x2={width} y2="0" className="stroke-gray-100" strokeDasharray="4" strokeWidth="1" />

        {/* The Line */}
        <polyline
          fill="none"
          strokeWidth="2"
          points={points}
          className={`${strokeColor} transition-all duration-500`}
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Dots */}
        {values.map((val, index) => {
          const x = (index / (values.length - 1)) * width;
          const padding = 10;
          const availableHeight = height - (padding * 2);
          const y = height - padding - (((val - min) / range) * availableHeight);

          return (
            <circle
              key={index}
              cx={x}
              cy={y}
              r="3"
              className="fill-white stroke-indigo-600 hover:r-4 transition-all"
              strokeWidth="2"
            >
              <title>{`${metric}: ${val}`}</title>
            </circle>
          );
        })}
      </svg>
    </div>
  );
};

export default HistoryChart;
