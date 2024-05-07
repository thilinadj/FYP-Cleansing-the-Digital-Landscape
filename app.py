import os
import joblib
from error_handler import *
from flask_cors import CORS
from cleanser import cleanser
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from shared_data.shared_data import UPLOAD_TEMP_FOLDER, UPLOAD_MAIN_FOLDER

xgb_model = joblib.load(r"models\xgb_model.pkl")

def is_allowed_file(filename):
  allowed_extensions = {'mp4'}
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

app = Flask('app')
app.config['UPLOAD_TEMP_FOLDER'] = UPLOAD_TEMP_FOLDER
app.config['UPLOAD_MAIN_FOLDER'] = UPLOAD_MAIN_FOLDER
os.makedirs(UPLOAD_TEMP_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_MAIN_FOLDER, exist_ok=True)
CORS(app, resource={r"/api/*": {"origins": "*"}})
app.config['CORS HEADERS'] = 'content-Type'

@app.route('/api/cleanse-video', methods=['POST'])
def cleanse_video():
  try:
    if 'file' not in request.files:
      raise NoFileError

    file = request.files['file']

    if file and is_allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_TEMP_FOLDER'], filename))

      filename_without_extention = os.path.splitext(filename)[0]

      try:
        cleanser(filename_without_extention, xgb_model)
      except InternalServerError as ise:
        return jsonify({"message": str(ise)}), 500
      
      return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    
    else:
      raise FileTypeNotSupported
  
  except NoFileError as nfe:
    return jsonify({"message": str(nfe)}), 400
  
  except FileTypeNotSupported as ftns:
    return jsonify({"message": str(ftns)}), 400

@app.route('/api/videos', methods=['GET'])
def list_video_titles():
    try:
        video_folder_path = app.config['UPLOAD_MAIN_FOLDER']
        files = os.listdir(video_folder_path)
        video_titles = [os.path.splitext(file)[0] for file in files if is_allowed_file(file)]
        return jsonify(video_titles), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/video/<title>', methods=['GET'])
def get_video_url(title):
    try:
        video_folder_path = app.config['UPLOAD_MAIN_FOLDER']
        video_files = [file for file in os.listdir(video_folder_path) if is_allowed_file(file)]

        for file in video_files:
            if os.path.splitext(file)[0] == title:
                filepath = os.path.join(video_folder_path, file)
                return send_file(filepath, mimetype='video/mp4')
            
        return jsonify({'error': 'Video not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()