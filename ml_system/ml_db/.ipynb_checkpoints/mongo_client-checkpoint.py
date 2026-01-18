from pymongo import MongoClient

MONGO_URI = ("mongodb+srv://vernekar337:sahil337" 
"@cluster0.eqfq30p.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = "DriftAnalysisSystem"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

prediction_logs_collection = db["prediction_logs"]
ground_truth_logger_collection = db["ground_truth"]