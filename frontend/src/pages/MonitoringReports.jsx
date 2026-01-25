import React, { useEffect, useState } from 'react';
import { FileText, AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import Table from '../components/ui/Table';
import { getMonitoringReports } from '../api/endpoints';

// TEMP_UI_ONLY: Mock Data

const MonitoringReports = () => {
  const [reports, setReports] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await getMonitoringReports();
        setReports(res.data);
      } catch (err) {
        console.error("Failed to fetch reports", err);
        // Fallback to mock data
        setReports(MOCK_REPORTS);
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  const BooleanIndicator = ({ value }) => (
    <div className="flex items-center gap-1.5">
      {value ? (
        <>
          <span className="text-gray-900 font-medium">Yes</span>
          <div className="w-2 h-2 rounded-full bg-indigo-500"></div>
        </>
      ) : (
        <span className="text-gray-400">No</span>
      )}
    </div>
  );

  if (loading) return <div className="p-10 text-center text-gray-500">Loading Reports...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Monitoring Reports</h1>
        <p className="text-sm text-gray-500">Historical monitoring and retraining activity</p>
      </div>

      <Card className="overflow-hidden">
        {reports && reports.length > 0 ? (
          <Table headers={[
            'Timestamp',
            'System Status',
            'Feature Drift',
            'Prediction Drift',
            'Perf. Degraded',
            'Retraining Triggered'
          ]}>
            {reports.map((report, idx) => (
              <tr key={idx} className="hover:bg-gray-50 transition-colors">
                <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6 border-b border-gray-100">
                  <div className="flex items-center gap-2">
                    <FileText size={16} className="text-gray-400" />
                    {new Date(report.timestamp).toLocaleString()}
                  </div>
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm border-b border-gray-100">
                  <Badge status={report.system_status} />
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm border-b border-gray-100">
                  <BooleanIndicator value={report.feature_drift_detected} />
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm border-b border-gray-100">
                  <BooleanIndicator value={report.prediction_drift_detected} />
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm border-b border-gray-100">
                  <BooleanIndicator value={report.performance_degraded} />
                </td>
                <td className="whitespace-nowrap px-3 py-4 text-sm border-b border-gray-100">
                  {report.retraining_triggered ? (
                    <Badge status="success" className="bg-indigo-50 text-indigo-700 ring-indigo-600/20">TRIGGERED</Badge>
                  ) : (
                    <span className="text-gray-400 text-sm">Skipped</span>
                  )}
                </td>
              </tr>
            ))}
          </Table>
        ) : (
          <div className="p-8 text-center text-gray-500">
            No historical reports found.
          </div>
        )}
      </Card>
    </div>
  );
};

export default MonitoringReports;
