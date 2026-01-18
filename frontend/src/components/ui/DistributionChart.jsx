import React from 'react';

const DistributionChart = ({ trainData = [], currentData = [] }) => {
  // Determine the max value across both datasets to normalize height
  const allValues = [...trainData, ...currentData];
  const maxVal = allValues.length > 0 ? Math.max(...allValues) : 1;

  // Helper to calculate percentage height
  const getHeight = (val) => `${(val / maxVal) * 100}%`;

  // Assuming trainData and currentData are equal length buckets
  const buckets = Array.from({ length: Math.max(trainData.length, currentData.length) });

  if (allValues.length === 0) {
    return <div className="h-40 flex items-center justify-center text-gray-400 text-sm">No distribution data</div>;
  }

  return (
    <div className="w-full">
      <div className="flex items-center gap-4 mb-4 text-xs">
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-indigo-300 rounded-sm"></div>
          <span className="text-gray-600">Training</span>
        </div>
        <div className="flex items-center gap-1">
          <div className="w-3 h-3 bg-indigo-600 rounded-sm"></div>
          <span className="text-gray-600">Current</span>
        </div>
      </div>

      <div className="h-48 flex items-end gap-1 sm:gap-2">
        {buckets.map((_, idx) => {
          const trainVal = trainData[idx] || 0;
          const currentVal = currentData[idx] || 0;

          return (
            <div key={idx} className="flex-1 flex gap-0.5 justify-center items-end h-full group relative">
              {/* Bars */}
              <div
                style={{ height: getHeight(trainVal) }}
                className="w-1/2 bg-indigo-300 rounded-tl-sm rounded-tr-sm transition-all duration-300 relative top-0"
              ></div>
              <div
                style={{ height: getHeight(currentVal) }}
                className="w-1/2 bg-indigo-600 rounded-tl-sm rounded-tr-sm transition-all duration-300 relative top-0"
              ></div>

              {/* Tooltip on hover */}
              <div className="absolute bottom-full mb-2 hidden group-hover:flex flex-col bg-slate-800 text-white text-xs p-2 rounded z-10 whitespace-nowrap">
                <div>Bucket {idx + 1}</div>
                <div>Train: {trainVal}</div>
                <div>Current: {currentVal}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default DistributionChart;
