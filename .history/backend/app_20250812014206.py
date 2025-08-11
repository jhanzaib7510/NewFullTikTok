from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fake in-memory database
videos_data = []

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Add to in-memory database
    videos_data.append({
        "title": file.filename,
        "url": f"/uploads/{file.filename}",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 0,
        "likes": 0
    })

    return jsonify({"message": "Video uploaded successfully"}), 200


@app.route('/videos', methods=['GET'])
def get_videos():
    """Return just filenames for the home page."""
    return jsonify([v["title"] for v in videos_data])


@app.route('/uploads/<path:filename>')
def serve_video(filename):
    """Serve uploaded video files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/
