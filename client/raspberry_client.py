import cv2
import numpy as np
import websockets
import asyncio
from yolov5 import detect  # YOLOv5 detection module

# Simulate GPS data
def get_gps_data():
    return {
        "latitude": np.random.uniform(-90, 90),
        "longitude": np.random.uniform(-180, 180),
        "speed": np.random.uniform(0, 100)
    }

# Perform object detection using YOLOv5
def detect_objects(frame):
    # Save the frame as an image
    cv2.imwrite("temp_frame.jpg", frame)
    
    # Run YOLOv5 detection
    results = detect.run(weights="yolov5s.pt", source="temp_frame.jpg", conf_thres=0.5)
    
    # Parse results (e.g., count passengers)
    passenger_count = 0
    for result in results:
        for detection in result.pred:
            class_id = int(detection[-1])
            if class_id == 0:  # Class ID 0 is for "person" in COCO dataset
                passenger_count += 1
    return passenger_count

# Simulate client sending data to server
async def send_data():
    uri = "ws://localhost:8765"  # Replace with your server address
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)  # Use webcam
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Perform object detection
            passenger_count = detect_objects(frame)
            gps_data = get_gps_data()

            # Send data to server
            data = {
                "frame": frame.tolist(),
                "passenger_count": passenger_count,
                "gps_data": gps_data
            }
            await websocket.send(str(data))
            await asyncio.sleep(1)  # Simulate real-time delay

# Run the client
asyncio.get_event_loop().run_until_complete(send_data())