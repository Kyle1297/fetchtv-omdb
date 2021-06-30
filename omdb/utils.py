import requests

def get_response(url, params) :
    """ 
    Handle GET response and convert to json.
    """
    response = requests.get(url, params)
    response.raise_for_status()
    data = response.json()

    return data