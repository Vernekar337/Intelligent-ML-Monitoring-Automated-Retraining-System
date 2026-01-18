import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import DriftAnalysis from './pages/DriftAnalysis';
import Retraining from './pages/Retraining';
import MonitoringReports from './pages/MonitoringReports';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="drift" element={<DriftAnalysis />} />
          <Route path="retraining" element={<Retraining />} />
          <Route path="reports" element={<MonitoringReports />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
