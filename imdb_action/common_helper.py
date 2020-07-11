import json

def http_response_smart(data, message="", status=""):
    return json.dumps({"data": data, "message": message, "status": status})