from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
import os
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load the YOLOv8 model (use your trained model path)
MODEL_PATH = "best.pt"  # Replace with your YOLOv8 model
model = YOLO(MODEL_PATH)

# Directory to save uploaded photos and results
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/process-photo', methods=['POST'])
def process_photo():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo provided"}), 400

    # Save the uploaded photo
    photo = request.files['photo']
    filename = f"{uuid.uuid4().hex}_{photo.filename}"
    photo_path = os.path.join(UPLOAD_FOLDER, filename)
    photo.save(photo_path)

    # Perform object detection
    try:
        results = model(photo_path)  # Perform inference
        result_path = os.path.join(RESULT_FOLDER, f"result_{filename}")
        results[0].plot(save=True, save_dir=RESULT_FOLDER)  # Save the processed image

        # Return the result URL
        return jsonify({
            "message": "Photo processed successfully",
            "result_url": f"/results/result_{filename}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/results/<filename>')
def get_result(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
