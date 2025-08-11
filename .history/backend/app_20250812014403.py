from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

# === CONFIG ===
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'webm'}
MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Upload video ---
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file found in request'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(save_path)

        return jsonify({
            'message': 'File uploaded successfully',
            'filename': unique_filename,
            'url': f"/uploads/{unique_filename}"
        }), 201

    return jsonify({'error': 'Invalid file type'}), 400

# --- List videos ---
@app.route('/videos', methods=['GET'])
def list_videos():
    files = sorted(
        os.listdir(app.config['UPLOAD_FOLDER']),
        key=lambda f: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], f)),
        reverse=True
    )
    return jsonify(files)

# --- Serve uploaded video ---
@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Get video info ---
@app.route('/video-info/<filename>', methods=['GET'])
def video_info(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        return jsonify({'error': 'File not found'}), 404

    stat = os.stat(path)
    return jsonify({
        'name': filename,
        'size_kb': round(stat.st_size / 1024, 2),
        'upload_time': datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    })

# --- Delete video ---
@app.route('/delete-video/<filename>', methods=['DELETE'])
def delete_video(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        return jsonify({'error': 'File not found'}), 404

    os.remove(path)
    return jsonify({'message': f'{filename} deleted successfully'})

# --- Dashboard API ---
@app.route('/dashboard', methods=['GET'])
def dashboard():
    files = sorted(
        os.listdir(app.config['UPLOAD_FOLDER']),
        key=lambda f: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], f)),
        reverse=True
    )

    total_videos = len(files)
    total_likes = total_videos * 10  # Dummy like count (replace with DB)
    total_views = total_videos * 120  # Dummy views count (replace with DB)

    recent_activity = []
    for f in files[:5]:
        stat = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], f))
        recent_activity.append({
            "type": "upload",
            "title": f,
            "time": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "url": f"/uploads/{f}"
        })

    return jsonify({
        "totalVideos": total_videos,
        "totalViews": total_views,
        "totalLikes": total_likes,
        "recentActivity": recent_activity
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)