from bson import ObjectId

def objectid_to_str(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, ObjectId):
                obj[key] = str(value)
            elif isinstance(value, (dict, list)):
                obj[key] = objectid_to_str(value)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            if isinstance(obj[i], ObjectId):
                obj[i] = str(obj[i])
            elif isinstance(obj[i], (dict, list)):
                obj[i] = objectid_to_str(obj[i])
    return obj