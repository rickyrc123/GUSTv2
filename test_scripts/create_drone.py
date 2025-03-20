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

    response = requests.post(url, params=params)
    return response.json()

if __name__ == "__main__":
    long_example = 0
    lat_example = 0
    alt_example = 0
    bearing_example = 0
    name_example = "TestDrone"
    model_example = "ModelX"

    result = create_drone(long_example, lat_example, alt_example, bearing_example, name_example, model_example)

    print(result)