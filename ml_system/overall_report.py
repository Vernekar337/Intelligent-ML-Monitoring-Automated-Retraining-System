from ml_db.mongo_client import overall_report_collection

def generate_overall_report(reports : dict) -> bool:
  if (reports["status"] == 'no_drift'):
    return False
  
  else:
    return True
  
  
def generate_feature_decision(reports : dict) -> bool:
  if(reports['summary']['overall_status'] == 'drift_detected'):
    return True;
  
  else:
    return False;
  
def generate_retraining_decision(report: dict) -> bool:
  if(report['decision'] == 'retrained'):
    return True
  
  else:
    return False
  
def generate_system_status(report: dict):
  return report['overall_status']
  
def generate_final_report(report : dict):
  overall_report_collection.insert_one(report)