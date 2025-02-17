import requests

def create_drone(longitude, latitude, altitude, bearing, name, model):
    url = "http://localhost:8000/drones/create"
    params = {
        "long": longitude,
        "lat": latitude,
        "alt": altitude,
        "bearing": bearing,
        "name": name,
        "model": model
    }

    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    long_example = 45.123
    lat_example = -93.456
    alt_example = 100.0
    bearing_example = 90
    name_example = "TestDrone"
    model_example = "ModelX"

    result = create_drone(long_example, lat_example, alt_example, bearing_example, name_example, model_example)

    print(result)