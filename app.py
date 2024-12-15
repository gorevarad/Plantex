from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()

# Load the YOLO model
model = YOLO('yolov8n.pt')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Perform prediction
    results = model(img)
    
    # Process results
    predictions = results[0].boxes.data
    class_names = results[0].names
    
    # Get the class with the highest confidence
    if len(predictions) > 0:
        best_prediction = predictions[predictions[:, 4].argmax()]
        class_id = int(best_prediction[5])
        confidence = float(best_prediction[4])
        class_name = class_names[class_id]
        
        return {"prediction": f"{class_name} ({confidence:.2f})"}
    else:
        return {"prediction": "No object detected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="127.0.0.1")
