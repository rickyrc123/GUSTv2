import requests
#gettin stuff from the API
def main():
    
    data = {
        "name": "drone1",
        "model": "string",
        "current_long": 87.564444,
        "current_lat": 33.209722,
        "current_alt": 61.5,
        "current_yaw": 0.0
    }
    
    data1 = {
        "name": "drone2",
        "model": "string",
        "current_long": 87.5821111,
        "current_lat": 33.22222222,
        "current_alt": 55.1,
        "current_yaw": 0.0
    }

    data2 = {
        "name": "drone3",
        "model": "string",
        "current_long": 87.434443,
        "current_lat": 33.252212,
        "current_alt": 33.1,
        "current_yaw": 0.0
    }
    response = requests.post(url="http://127.0.0.1:8000/drones/create", json=data)
    response.raise_for_status()
    print(response.text)

    response = requests.post(url="http://127.0.0.1:8000/drones/create", json=data1)
    response.raise_for_status()
    print(response.text)

    response = requests.post(url="http://127.0.0.1:8000/drones/create", json=data2)
    response.raise_for_status()
    print(response.text)



    

main()