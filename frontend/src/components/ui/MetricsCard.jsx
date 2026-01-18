import React from 'react';
import Card from './Card';

const MetricsCard = ({ title, value, subtext, trend }) => {
  return (
    <Card className="flex flex-col justify-between h-full">
      <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
      <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">{value}</dd>
      {(subtext || trend) && (
        <div className="mt-2 flex items-center text-sm">
          {trend && (
            <span className={`font-medium ${trend.isPositive ? 'text-green-600' : 'text-red-600'}`}>
              {trend.value}
            </span>
          )}
          {subtext && <span className="text-gray-500 ml-2">{subtext}</span>}
        </div>
      )}
    </Card>
  );
};

export default MetricsCard;
