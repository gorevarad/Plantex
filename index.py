from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/process-photo', methods=['POST'])
def process_photo():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo provided"}), 400
    
    photo = request.files['photo']
    photo_path = os.path.join("uploads", photo.filename)
    os.makedirs("uploads", exist_ok=True)
    photo.save(photo_path)

    # Example: Processing logic
    result = {"message": "Photo received and processed!", "filename": photo.filename}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
