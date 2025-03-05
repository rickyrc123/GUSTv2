import requests
#gettin stuff from the API
def main():
    
    data = {
        "name": "boberto",
        "model": "string",
        "current_long": 0.0,
        "current_lat": 0.0,
        "current_alt": 0.0,
        "current_yaw": 0.0
    }
    data1 = {
        "name": "boberto1",
        "model": "string",
        "current_long": 0.0,
        "current_lat": 0.0,
        "current_alt": 0.0,
        "current_yaw": 0.0
    }
    response = requests.post(url="http://127.0.0.1:8000/drones/create", json=data)
    response.raise_for_status()

    print(response.text)

    response = requests.post(url="http://127.0.0.1:8000/drones/create", json=data1)
    response.raise_for_status()

    print(response.text)

    name = data["name"]
    response = requests.post(url=f"http://127.0.0.1:8000/drones/{name}/delete")
    response.raise_for_status()

    data = {
     "name" : "boberto1",
     "model": "t",
     "current_long"  : 32.1,
     "current_lat"  : 21.2,
     "current_alt"  : 22.1,
     "current_yaw"  : 5.2
    }

    response = requests.post(url=f"http://127.0.0.1:8000/drones/{data["name"]}/post_position", json=data)

    print(response.text)

    response = requests.get(url=f"http://127.0.0.1:8000/drones/{data["name"]}/post_position", json=data)
main()