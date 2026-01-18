from bson import ObjectId

def serialize_object(obj):
  
  if isinstance(obj, ObjectId):
    return str(obj)
  
  elif isinstance(obj, dict):
    return {k : serialize_object(v) for k, v in obj.items()}
  
  elif isinstance(obj, list):
    return [serialize_object(items) for items in obj]
  
  return obj
  
  