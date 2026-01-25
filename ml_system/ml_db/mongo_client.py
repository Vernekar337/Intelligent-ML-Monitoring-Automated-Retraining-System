from pymongo import MongoClient

MONGO_URI = ("mongodb+srv://vernekar337:sahil337" 
"@cluster0.eqfq30p.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = "DriftAnalysisSystem"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

prediction_logs_collection = db["prediction_logs"]
ground_truth_logger_collection = db["ground_truth"]
prediction_drift_report_collection = db["prediction_drift_report"]
temp_prediction_log_collection = db["temp_prediction_log"]
performance_drift_reports_collection = db["performance_drift_reports"]
feature_drift_reports_collection = db['feature_drift_reports']
model_health_reports_collection = db['model_health_reports']
retraining_decisions_collection = db['retraining_decisions']
model_registry_collection = db['model_registry']
overall_report_collection = db['overall_reports']