from fastapi import FastAPI, WebSocket
import numpy as np
import asyncio
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = eval(data)  # Convert string to dictionary

        frame = np.array(data["frame"])
        passenger_count = data["passenger_count"]
        gps_data = data["gps_data"]

        # Check for abnormal conditions (e.g., too many passengers)
        if passenger_count > 50:
            print("Abnormal condition detected!")

        # Store data in database (simulated)
        store_data(gps_data, passenger_count)

def store_data(gps_data, passenger_count):
    # Simulate storing data in a database
    print(f"Stored data: {gps_data}, Passenger Count: {passenger_count}")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8765)