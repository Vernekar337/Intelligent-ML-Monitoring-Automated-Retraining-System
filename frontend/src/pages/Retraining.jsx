import React, { useEffect, useState } from 'react';
import { CheckCircle, XCircle, AlertCircle, Play } from 'lucide-react';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { getRetrainingDecision, triggerRetraining } from '../api/endpoints';

const Retraining = () => {
  const [decision, setDecision] = useState(null);
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetchDecision();
  }, []);

  const fetchDecision = async () => {
    try {
      const res = await getRetrainingDecision();
      setDecision(res.data);
    } catch (err) {
      console.error("Failed to fetch retraining decision", err);
    } finally {
      setLoading(false);
    }
  };

  const handleTrigger = async () => {
    setTriggering(true);
    setMessage(null);
    try {
      const res = await triggerRetraining();
      setMessage({ type: 'success', text: res.data.message || 'Retraining triggered successfully' });
      // Refresh decision state
      fetchDecision();
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to trigger retraining' });
    } finally {
      setTriggering(false);
    }
  };

  if (loading) return <div className="p-10 text-center text-gray-500">Evaluating Decision Logic...</div>;

  const DecisionItem = ({ label, value, description }) => (
    <div className="flex items-center justify-between py-4 border-b border-gray-100 last:border-0">
      <div className="flex flex-col">
        <span className="text-sm font-medium text-gray-900">{label}</span>
        {description && <span className="text-xs text-gray-500">{description}</span>}
      </div>
      <div className="flex items-center gap-2">
        <span className={`text-sm font-medium ${value ? 'text-indigo-600' : 'text-gray-400'}`}>
          {value ? 'YES' : 'NO'}
        </span>
        {value ? <CheckCircle size={18} className="text-indigo-600" /> : <XCircle size={18} className="text-gray-300" />}
      </div>
    </div>
  );

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">Retraining Decision Engine</h1>
        <p className="text-sm text-gray-500 mt-2">Automated evaluation logic for model updates</p>
      </div>

      {decision && (
        <Card className="overflow-hidden">
          <div className={`p-6 text-center border-b ${decision.retraining_triggered ? 'bg-indigo-50 border-indigo-100' : 'bg-gray-50 border-gray-100'}`}>
            <p className="text-xs uppercase tracking-wider font-semibold text-gray-500 mb-2">Detailed Status</p>
            <h2 className={`text-3xl font-bold ${decision.retraining_triggered ? 'text-indigo-700' : 'text-gray-700'}`}>
              {decision.retraining_triggered ? 'RETRAINING TRIGGERED' : 'NO ACTION REQUIRED'}
            </h2>
          </div>

          <div className="p-8">
            <h3 className="text-sm font-semibold text-gray-900 mb-4 uppercase tracking-wide">Decision Factors</h3>
            <div className="space-y-1">
              <DecisionItem
                label="Feature Drift Detected"
                value={decision.feature_drift_detected}
                description="Significant distribution shift in input features"
              />
              <DecisionItem
                label="Prediction Drift Detected"
                value={decision.prediction_drift_detected}
                description="Significant shift in model output distribution"
              />
              <DecisionItem
                label="Performance Degraded"
                value={decision.performance_degraded}
                description="Metric drops below critical thresholds"
              />
              <DecisionItem
                label="Cooldown Active"
                value={decision.cooldown_active}
                description="Minimum time between training runs enforcement"
              />
              <DecisionItem
                label="Data Sufficient"
                value={decision.data_sufficient}
                description="Enough new data available for training"
              />
            </div>
          </div>

          <div className="p-6 bg-gray-50 border-t border-gray-100 flex flex-col items-center gap-4">
            {message && (
              <div className={`text-sm p-2 rounded ${message.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                {message.text}
              </div>
            )}

            <div className="flex items-center gap-4">
              <Button
                disabled={!decision.manual_trigger_allowed || triggering}
                onClick={handleTrigger}
                className="w-full sm:w-auto flex items-center gap-2"
              >
                {triggering ? <Activity className="animate-spin" size={16} /> : <Play size={16} />}
                Trigger Manual Retraining
              </Button>
              {!decision.manual_trigger_allowed && (
                <span className="text-xs text-gray-400 max-w-xs text-center">
                  Manual triggering is currently disabled by system policy or active cooldown.
                </span>
              )}
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

export default Retraining;
