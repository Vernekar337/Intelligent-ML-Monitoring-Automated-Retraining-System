import apiClient from './client';

export const getSystemHealth = () => apiClient.get('/monitoring/system/health');

export const getFeatureDrift = () => apiClient.get('/monitoring/feature-drift');

export const getPredictionDrift = () => apiClient.get('/monitoring/prediction-drift');

export const getModelPerformance = () => apiClient.get('/monitoring/performance');

export const getRetrainingDecision = () => apiClient.get('/monitoring/retraining-decision');

export const getMonitoringReports = () => apiClient.get('/monitoring/reports');

export const triggerRetraining = () => apiClient.post('/monitoring/retrain');
