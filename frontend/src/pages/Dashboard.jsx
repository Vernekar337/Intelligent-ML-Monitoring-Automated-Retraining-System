import React, { useEffect, useState } from 'react';
import { Activity, Clock, AlertTriangle, CheckCircle, Smartphone, ShieldCheck } from 'lucide-react';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import MetricsCard from '../components/ui/MetricsCard';
import HistoryChart from '../components/ui/HistoryChart'; // Import HistoryChart
import { getSystemHealth, getModelPerformance, getFeatureDrift, getPredictionDrift } from '../api/endpoints';

// TEMP_UI_ONLY: Mock Data
const MOCK_HEALTH = {
  model_version: "v2.3.1",
  system_status: "healthy",
  last_pipeline_run: "2023-10-27T14:30:00Z",
  retraining_recommended: false,
  cooldown_active: false
};

const MOCK_PERFORMANCE = {
  model_version: "v2.3.1",
  metrics: {
    accuracy: 0.945,
    precision: 0.912,
    recall: 0.887,
    f1: 0.899
  },
  history: [
    { timestamp: "2023-10-20", accuracy: 0.920 },
    { timestamp: "2023-10-21", accuracy: 0.925 },
    { timestamp: "2023-10-22", accuracy: 0.930 },
    { timestamp: "2023-10-23", accuracy: 0.928 },
    { timestamp: "2023-10-24", accuracy: 0.935 },
    { timestamp: "2023-10-25", accuracy: 0.942 },
    { timestamp: "2023-10-26", accuracy: 0.940 },
    { timestamp: "2023-10-27", accuracy: 0.945 }
  ]
};

const MOCK_FEATURE_DRIFT = {
  model_version: "v2.3.1",
  window: "last_7_days",
  features: [
    { name: "account_tenure_days", psi: 0.62, status: "critical" },
    { name: "avg_transaction_val", psi: 0.35, status: "warning" },
    { name: "daily_active_mins", psi: 0.18, status: "warning" },
    { name: "customer_age", psi: 0.05, status: "ok" }
  ]
};

const MOCK_PRED_DRIFT = {
  model_version: "v2.3.1",
  psi: 0.34,
  status: "warning",
  distribution: { train: [], current: [] } // Dashboard only needs Summary status usually
};

const Dashboard = () => {
  const [health, setHealth] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [featureDrift, setFeatureDrift] = useState(null);
  const [predDrift, setPredDrift] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [healthRes, perfRes, fDriftRes, pDriftRes] = await Promise.allSettled([
          getSystemHealth(),
          getModelPerformance(),
          getFeatureDrift(),
          getPredictionDrift()
        ]);

        // Health Logic (Mock Fallback)
        if (healthRes.status === 'fulfilled' && healthRes.value.data) {
          setHealth(healthRes.value.data);
        } else {
          setHealth(MOCK_HEALTH);
        }

        // Performance Logic (Mock Fallback)
        if (perfRes.status === 'fulfilled' && perfRes.value.data) {
          setPerformance(perfRes.value.data);
        } else {
          setPerformance(MOCK_PERFORMANCE);
        }

        // Feature Drift Logic (Mock Fallback)
        if (fDriftRes.status === 'fulfilled' && fDriftRes.value.data) {
          setFeatureDrift(fDriftRes.value.data);
        } else {
          setFeatureDrift(MOCK_FEATURE_DRIFT);
        }

        // Prediction Drift Logic (Mock Fallback)
        if (pDriftRes.status === 'fulfilled' && pDriftRes.value.data) {
          setPredDrift(pDriftRes.value.data);
        } else {
          setPredDrift(MOCK_PRED_DRIFT);
        }

      } catch (err) {
        console.error("Critical error in dashboard data fetch", err);
        // Ensure UI still renders mocks even on catastrophic failure
        setHealth(MOCK_HEALTH);
        setPerformance(MOCK_PERFORMANCE);
        setFeatureDrift(MOCK_FEATURE_DRIFT);
        setPredDrift(MOCK_PRED_DRIFT);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center p-10">
        <div className="text-gray-500 flex flex-col items-center">
          <Activity className="animate-spin mb-4" size={32} />
          <p>Loading System Telemetry...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">System Overview</h1>
          <p className="text-sm text-gray-500">Real-time model monitoring status</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">Last updated: {new Date().toLocaleTimeString()}</span>
        </div>
      </div>

      {/* Top Status Cards */}
      {health && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="flex flex-col justify-center">
            <div className="text-sm text-gray-500 mb-1">System Status</div>
            <div className="flex items-center justify-between">
              <span className="text-lg font-semibold text-gray-900 capitalize">{health.system_status}</span>
              <Badge status={health.system_status} />
            </div>
          </Card>

          <Card className="flex flex-col justify-center">
            <div className="text-sm text-gray-500 mb-1">Active Model Version</div>
            <div className="flex items-center gap-2">
              <ShieldCheck size={20} className="text-indigo-600" />
              <span className="text-lg font-semibold text-gray-900">{health.model_version}</span>
            </div>
          </Card>

          <Card className="flex flex-col justify-center">
            <div className="text-sm text-gray-500 mb-1">Last Pipeline Run</div>
            <div className="flex items-center gap-2">
              <Clock size={20} className="text-gray-400" />
              <span className="text-lg font-semibold text-gray-900">
                {new Date(health.last_pipeline_run).toLocaleDateString()}
              </span>
            </div>
          </Card>

          <Card className="flex flex-col justify-center">
            <div className="text-sm text-gray-500 mb-1">Retraining Status</div>
            <div className="flex items-center gap-2">
              {health.retraining_recommended ? (
                <Badge status="warning" className="bg-yellow-100 text-yellow-800">RECOMMENDED</Badge>
              ) : (
                <Badge status="ok" className="bg-gray-100 text-gray-600">NOT REQUIRED</Badge>
              )}
            </div>
            {health.cooldown_active && (
              <span className="text-xs text-gray-400 mt-1">Cooldown Active</span>
            )}
          </Card>
        </div>
      )}

      {/* Detailed Sections Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Model Performance */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Model Performance</h2>
          </div>

          {performance ? (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <MetricsCard title="Accuracy" value={performance.metrics.accuracy?.toFixed(3)} />
              <MetricsCard title="Precision" value={performance.metrics.precision?.toFixed(3)} />
              <MetricsCard title="Recall" value={performance.metrics.recall?.toFixed(3)} />
              <MetricsCard title="F1 Score" value={performance.metrics.f1?.toFixed(3)} />
            </div>
          ) : (
            <Card><p className="text-gray-400 text-center py-4">No performance data available</p></Card>
          )}

          {/* Performance History */}
          <Card title="Performance Trends (Accuracy)">
            <div className="h-64 flex items-center justify-center p-4">
              {performance?.history ? (
                <HistoryChart data={performance.history} metric="accuracy" />
              ) : (
                <p className="text-gray-400 text-sm">No history data available</p>
              )}
            </div>
          </Card>
        </div>

        {/* Drift Summary Sidebar */}
        <div className="space-y-6">
          <h2 className="text-lg font-semibold text-gray-900">Drift Status</h2>

          <Card title="Feature Drift">
            {featureDrift ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Window</span>
                  <span className="text-sm font-medium">{featureDrift.window}</span>
                </div>
                <div className="grid grid-cols-1 gap-2">
                  {featureDrift.features?.slice(0, 5).map(f => (
                    <div key={f.name} className="flex items-center justify-between p-2 bg-gray-50 rounded text-sm">
                      <span className="truncate max-w-[120px]" title={f.name}>{f.name}</span>
                      <Badge status={f.status} />
                    </div>
                  ))}
                </div>
              </div>
            ) : <p className="text-gray-400 text-sm">No drift data</p>}
          </Card>

          <Card title="Prediction Drift">
            {predDrift ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Overall Status</span>
                  <Badge status={predDrift.status} />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">PSI Score</span>
                  <span className="text-lg font-mono font-medium">{predDrift.psi?.toFixed(3)}</span>
                </div>
              </div>
            ) : <p className="text-gray-400 text-sm">No drift data</p>}
          </Card>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
