import asyncio
import random
import json
import time
from websockets.asyncio.client import connect

# fake drone list
DRONE_IDS = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
]


# creates mock gps data for a random drone from the given list.
# function can provide a specified range of coordinates if provided, or random.
def generate_random_data(
    num_positions = None
):
    
    position_array = []

    #if no range specified, make it random
    if num_positions is None: 
        num_positions = random.randint(1,25)

    for _ in range(0, num_positions):

        # random position coordinates, longitude, latitude, and Altitude
        rand_long  =  random.uniform( -180,  180 )
        rand_lat   =  random.uniform(  -90,  90  )
        rand_alt   =  random.uniform(    0,  50  )

        position_array.append({
           "long"           : rand_long, 
           "lat"            : rand_lat,
           "alt_meters"     : rand_alt
        })
    
    # convert to json payload
    # websocket messages must be btyes or strings

    payload = {
        "coordinates" : position_array,
        "drone_id"    : random.choice(DRONE_IDS),
        "message"     : "WARNING!: This is randomly generated data!"
    }

    return json.dumps(payload, indent=4)


#sends the data
async def send_mock_data():

    async with connect("ws://localhost:8765") as websocket:

        # sends data to server, the server must be running in another terminal
        while(1):
            time.sleep(random.uniform(1,5))
            await websocket.send(generate_random_data(10))

            # prints the data that is recieved by the server
            message = await websocket.recv()    
            print(message)


async def main():
    send_mock_data()

if __name__ == "__main__":
    asyncio.run(send_mock_data())