import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import subprocess
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'wav', 'mp3'}

load_dotenv()  # Load environment variables from .env file
MODEL_PATH = os.getenv('MODEL_PATH')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

logging.basicConfig(level=logging.DEBUG)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if file and allowed_file(file.filename):
            input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_file_path)
            output_format = request.form.get('output_format', 'csv')
            output_file_name = f"{os.path.splitext(file.filename)[0]}.{output_format}"
            output_file_path = os.path.join(app.config['PROCESSED_FOLDER'], output_file_name)
            
            # Log debug information to the console
            logging.debug(f'Input file path: {input_file_path}')
            logging.debug(f'Model path: {MODEL_PATH}')
            logging.debug(f'Output file path: {output_file_path}')
            logging.debug(f'Output format: {output_format}')
            
            # Run the main.py script using Thonburian_venv
            venv_python = os.path.join('Thonburian_venv', 'Scripts', 'python.exe')
            process = subprocess.run(
                [venv_python, 'main.py', '--input_file', input_file_path, '--output_file', output_file_path, '--model_path', MODEL_PATH, '--output_format', output_format],
                capture_output=True,
                text=True
            )
            
            if process.returncode == 0:
                return jsonify({
                    'success': True,
                    'message': 'File processed successfully',
                    'output_filename': output_file_name,
                    'download_url': url_for('download_file', filename=output_file_name, _external=True)
                }), 200
            else:
                return jsonify({
                    'error': 'Processing failed',
                    'details': process.stderr
                }), 500
                
        return jsonify({'error': 'File type not allowed'}), 400
        
    except Exception as e:
        logging.error(f'Error processing upload: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)