import asyncio
from websockets.asyncio.server import serve

#prints data
async def echo(websocket):
    async for message in websocket:
        print(f"recieved message:{message}")
        # do something with the data....

        # send a response....
        await websocket.send(message)

#open websocket on a port 8765
async def main():
    print("sending data")
    async with serve(echo, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

