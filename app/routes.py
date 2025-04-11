import os
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from app.exif_handler import get_exif_data, update_exif_data, remove_exif_data

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Generate a unique filename to prevent overwrites
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract EXIF data
        exif_data = get_exif_data(file_path)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'exif_data': exif_data
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@main_bp.route('/exif/<filename>', methods=['GET'])
def get_exif(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    exif_data = get_exif_data(file_path)
    return jsonify(exif_data)

@main_bp.route('/exif/<filename>', methods=['PUT'])
def update_exif(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # Get the updated EXIF data from the request
    updated_exif = request.json
    
    # Update the EXIF data in the image
    success = update_exif_data(file_path, updated_exif)
    
    if success:
        return jsonify({'success': True, 'message': 'EXIF data updated successfully'})
    else:
        return jsonify({'error': 'Failed to update EXIF data'}), 500

@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/exif/<filename>/remove', methods=['POST'])
def remove_exif(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # Remove EXIF data from the image
    success = remove_exif_data(file_path)
    
    if success:
        return jsonify({'success': True, 'message': 'EXIF data removed successfully'})
    else:
        return jsonify({'error': 'Failed to remove EXIF data'}), 500 