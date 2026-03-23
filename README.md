# Intelligent ML Monitoring & Automated Retraining System

## Overview

A production-style MLOps system designed to monitor deployed machine learning models, detect drift, and automatically trigger retraining using policy-driven decision logic.

This project focuses on **building a complete ML lifecycle system** rather than just training a model, covering monitoring, evaluation, retraining, and deployment workflows.

---

## Problem Statement

Machine learning models degrade over time due to changes in data distribution and real-world conditions.

Most systems lack:

* Continuous performance monitoring
* Drift detection mechanisms
* Automated retraining pipelines
* Explainability for retraining decisions

---

## Solution

This system provides:

* Real-time monitoring of model performance
* Feature and prediction drift detection
* Policy-driven automated retraining
* Model versioning and lifecycle management
* Explainable retraining decisions

---

## Key Highlights

* End-to-end ML lifecycle system (inference → monitoring → retraining)
* PSI-based feature and prediction drift detection
* Policy-driven retraining with cooldown and validation checks
* Model registry with versioning and performance tracking
* Automated retraining pipeline with temporal validation
* Explainable decision engine for retraining triggers
* Real-time monitoring dashboard

---

## System Architecture

```id="mlarch"
Inference → Logging → Monitoring → Health Report → Decision Engine → Retraining → Registry
```

---

## Core Components

### Inference Pipeline

* Generates predictions and logs metadata for monitoring

### Ground Truth Logging

* Stores actual outcomes for post-deployment evaluation

### Monitoring Pipelines

* Feature Drift Detection (PSI-based)
* Prediction Drift Detection
* Performance Monitoring (Accuracy, Precision, Recall, F1)

### Health Report Engine

* Aggregates monitoring signals
* Determines system status (healthy / warning / critical)

### Retraining Decision Engine

* Evaluates retraining triggers based on:

  * Drift signals
  * Performance degradation
  * Cooldown constraints
  * Data sufficiency

### Retraining Pipeline

* Builds dataset from historical logs
* Trains and validates new models
* Updates model registry

### Model Registry

* Stores model versions, metadata, and metrics

### Policy Management

* Configurable rules for retraining behavior

### Dashboard

* Visualizes system health, drift, and retraining activity

---

## Tech Stack

### Backend

* FastAPI
* Python
* MongoDB

### Machine Learning

* Scikit-learn
* Pandas
* NumPy

### Frontend

* React.js
* Tailwind CSS

---

## Retraining Logic

Retraining is triggered only when:

* Drift or performance degradation is detected
* Cooldown period has passed
* Sufficient labeled data is available
* New model passes validation checks

Manual retraining requests are validated and return clear feedback if conditions are not met.

---

## API Endpoints

### Monitoring

* GET /monitoring/system/health
* GET /monitoring/performance
* GET /monitoring/feature-drift
* GET /monitoring/prediction-drift
* GET /monitoring/reports

### Retraining

* GET /monitoring/retraining-decision
* POST /monitoring/retrain

### Policy

* GET /monitoring/retraining-policy
* PUT /monitoring/retraining-policy

### Inference

* POST /inference/predict

---

## Project Structure

```id="mlstruct"
backend/
  inference/
  monitoring/
  retraining/
  registry/
  policy/
  utils/

frontend/
  components/
  pages/
  api/
  utils/

model/
  model_v1.pkl
  preprocessor.pkl
```

---

## How to Run

### Backend

```id="mlrun1"
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```id="mlrun2"
npm install
npm run dev
```

---

## Design Principles

* Separation of monitoring, decision, and execution layers
* Backend-driven logic (no frontend decision-making)
* Explainability for automated actions
* Policy-driven system behavior
* Fail-safe retraining with validation checks
* Modular and extensible architecture

---

## Future Improvements

* Alerting system (email / Slack)
* Model explainability (SHAP, feature importance)
* Automated rollback on performance drop
* CI/CD pipeline for model deployment
* Distributed processing for large-scale data

---

## Author

Sahil Sandeep Vernekar

---

## Note

This project is designed to demonstrate:

* MLOps system design
* Monitoring and drift detection pipelines
* Automated retraining workflows

It is not a production deployment system.
