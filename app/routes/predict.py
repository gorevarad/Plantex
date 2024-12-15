from fastapi import APIRouter, File, UploadFile
from ultralytics import hub, YOLO, hub
import cv2
import numpy as np
import torch

router = APIRouter()

# Load the YOLO model

model = YOLO('plantex1.pt')


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
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
