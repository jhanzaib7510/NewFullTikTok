from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory "database"
videos_data = []

# -----------------------
# UPLOAD VIDEO
# -----------------------
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    videos_data.append({
        "title": file.filename,
        "url": f"/uploads/{file.filename}",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 0,
        "likes": 0
    })

    return jsonify({"message": "Video uploaded successfully"}), 200

# -----------------------
# GET ALL VIDEOS (Home)
# -----------------------
@app.route('/videos', methods=['GET'])
def get_videos():
    return jsonify([v["title"] for v in videos_data])

# -----------------------
# SERVE VIDEO FILES
# -----------------------
@app.route('/uploads/<path:filename>')
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# -----------------------
# DASHBOARD DATA
# -----------------------
@app.route('/dashboard', methods=['GET'])
def dashboard():
    total_videos = len(videos_data)
    total_views = sum(v["views"] for v in videos_data)
    total_likes = sum(v["likes"] for v in videos_data)

    return jsonify({
        "totalVideos": total_videos,
        "totalViews": total_views,
        "totalLikes": total_likes,
        "recentActivity": videos_data[-5:]  # last 5 uploads
    })

# -----------------------
# RUN SERVER
# -----------------------
if __name__ == '__main__':
    app.run(port=5000, debug=True)
