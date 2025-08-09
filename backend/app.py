from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video part'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected video'}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return jsonify({'message': 'Upload successful', 'filename': file.filename})

@app.route('/videos', methods=['GET'])
def get_videos():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/video-info/<filename>', methods=['GET'])
def video_info(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        return jsonify({'error': 'File not found'}), 404

    size_kb = round(os.path.getsize(path) / 1024, 2)
    return jsonify({'name': filename, 'size': size_kb})

@app.route('/delete-video/<filename>', methods=['DELETE'])
def delete_video(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        return jsonify({'error': 'File not found'}), 404

    os.remove(path)
    return jsonify({'message': f'{filename} deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
