import requests

#gettin stuff from the API
def main():
    
    data = {
        "name": "bob",
        "model": "string",
        "current_long": 0.0,
        "current_lat": 0.0,
        "current_alt": 0.0,
        "current_yaw": 0.0
    }

    response = requests.post(url="http://127.0.0.1:8000/drones/create", json=data)
    response.raise_for_status()

    print(response.text)
main()