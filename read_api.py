def readAPI(url):
    
    import requests
    import json
    
    response = requests.get(url)
    json_data = json.loads(response.content)

    return json_data 