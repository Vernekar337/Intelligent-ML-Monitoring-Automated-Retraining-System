import React, { useEffect, useState } from 'react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import Table from '../components/ui/Table';
import DistributionChart from '../components/ui/DistributionChart';
import { getFeatureDrift, getPredictionDrift } from '../api/endpoints';

// TEMP_UI_ONLY: Mock data for visualization
const MOCK_FEATURE_DRIFT = {
  model_version: "v1",
  window: "last_7_days",
  features: [
    { name: "account_tenure_days", psi: 0.62, status: "critical" },
    { name: "avg_transaction_val", psi: 0.35, status: "warning" },
    { name: "daily_active_mins", psi: 0.18, status: "warning" },
    { name: "customer_age", psi: 0.05, status: "ok" },
    { name: "num_support_tickets", psi: 0.02, status: "ok" },
    { name: "last_login_device", psi: 0.12, status: "ok" },
    { name: "marketing_opt_in", psi: 0.01, status: "ok" },
    { name: "region_code", psi: 0.08, status: "ok" }
  ]
};

const MOCK_PREDICTION_DRIFT = {
  model_version: "v1",
  psi: 0.34,
  status: "warning",
  distribution: {
    // Simulated bimodal distribution shift
    train: [15, 30, 45, 60, 80, 65, 40, 20, 10, 5],
    current: [10, 25, 40, 50, 40, 60, 80, 65, 30, 15]
  }
};

const DriftAnalysis = () => {
  const [featureDrift, setFeatureDrift] = useState(null);
  const [predDrift, setPredDrift] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [fDriftRes, pDriftRes] = await Promise.allSettled([
          getFeatureDrift(),
          getPredictionDrift()
        ]);

        // Use API data if available, otherwise fallback to MOCK
        if (fDriftRes.status === 'fulfilled' && fDriftRes.value.data) {
          setFeatureDrift(fDriftRes.value.data);
        } else {
          console.warn("Using MOCK Feature Drift Data");
          setFeatureDrift(MOCK_FEATURE_DRIFT);
        }

        if (pDriftRes.status === 'fulfilled' && pDriftRes.value.data) {
          setPredDrift(pDriftRes.value.data);
        } else {
          console.warn("Using MOCK Prediction Drift Data");
          setPredDrift(MOCK_PREDICTION_DRIFT);
        }
      } catch (err) {
        console.error("Failed to fetch drift data", err);
        // If Promise.allSettled itself fails (e.g., network error before any promise starts),
        // we still want to show mock data.
        setFeatureDrift(MOCK_FEATURE_DRIFT);
        setPredDrift(MOCK_PREDICTION_DRIFT);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="p-10 text-center text-gray-500">Loading Analysis...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Drift Analysis</h1>
        <p className="text-sm text-gray-500">Deep dive into feature and prediction stability</p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
        {/* Feature Drift Section */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Feature Drift</h2>
            {featureDrift && <span className="text-xs text-gray-500">Window: {featureDrift.window}</span>}
          </div>
          <Card className="overflow-hidden">
            {featureDrift ? (
              <Table headers={['Feature Name', 'PSI', 'Status']}>
                {featureDrift.features.map((feature, idx) => (
                  <tr key={idx} className="hover:bg-gray-50 transition-colors">
                    <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6 border-b border-gray-100">
                      {feature.name}
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 font-mono border-b border-gray-100">
                      {feature.psi?.toFixed(2)}
                    </td>
                    <td className="whitespace-nowrap px-3 py-4 text-sm border-b border-gray-100">
                      <Badge status={feature.status} />
                    </td>
                  </tr>
                ))}
              </Table>
            ) : <p className="p-4 text-gray-500">No feature data available.</p>}
          </Card>
        </div>

        {/* Prediction Drift Section */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">Prediction Drift</h2>
          {predDrift && (
            <div className="space-y-6">
              <Card className="flex items-center justify-between p-6 bg-gradient-to-r from-gray-50 to-white">
                <div>
                  <p className="text-sm font-medium text-gray-500">PSI Score</p>
                  <div className="flex items-baseline gap-2">
                    <p className="text-3xl font-bold text-gray-900 mt-1">{predDrift.psi?.toFixed(2)}</p>
                    <Badge status={predDrift.status} className="text-xs px-2 py-0.5" />
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-2 mb-1 justify-end">
                    <div className="w-3 h-3 bg-indigo-300 rounded-sm"></div>
                    <span className="text-xs text-gray-600">Training</span>
                  </div>
                  <div className="flex items-center gap-2 justify-end">
                    <div className="w-3 h-3 bg-indigo-600 rounded-sm"></div>
                    <span className="text-xs text-gray-600">Current</span>
                  </div>
                </div>
              </Card>

              <Card title="Distribution Comparison">
                <div className="mt-6 px-2">
                  <DistributionChart
                    trainData={predDrift.distribution.train}
                    currentData={predDrift.distribution.current}
                  />
                  <p className="text-xs text-center text-gray-400 mt-4">
                    Probability Density Buckets (0.0 - 1.0)
                  </p>
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DriftAnalysis;
