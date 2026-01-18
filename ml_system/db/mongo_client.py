from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ml_monitoring"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

prediction_logs_collection = db["prediction_logs"]
