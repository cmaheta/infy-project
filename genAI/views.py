from flask import Flask, Blueprint, session,flash, jsonify,render_template, request, redirect, url_for, send_from_directory
from util import create_folders, process_files,get_input_folder, get_output_folder, list_download_files
import os
import json
from docx import Document
from werkzeug.utils import secure_filename


views = Blueprint(__name__, "views")

@views.route('/')
def home():
    return render_template('ai_processes.html')

@views.route('/ai-processes' , methods=['POST'])
def ai_processes():
    if request.method == 'POST':
        process_type = request.form.get('process-type')
        if process_type:
            session['process_type'] = process_type
        
        if 'files[]' not in request.files:
            flash("No files selected.")
            return render_template('ai_downloads.html', files=[])
        else:
            files = request.files.getlist('files[]')
            create_folders()
            process_files(files, process_type)
            files = list_download_files()
    status = {"progress": 0, "message": "Process started"}
    return jsonify(status)       

@views.route('/ai-download-file/<filename>', methods=['GET'])
def ai_download_file(filename):
    return send_from_directory(get_output_folder(), filename, as_attachment=True)

@views.route('/preview/<filename>')
def preview_file(filename):
    try:
        if os.path.splitext(filename)[1].lower() == '.docx':
            doc = Document(get_input_folder()+filename)
            content = ''
            for paragraph in doc.paragraphs:
                content += paragraph.text
                content += "\n"
        else:        
            with open(os.path.join(get_output_folder(), filename), 'r') as file:
                content = file.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)})    

@views.route('/delete-file/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        process_type = request.form.get('process-type')
        if process_type:
            session['process_type'] = process_type
        file_path = os.path.join(get_output_folder(), filename)
        print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": f"{filename} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@views.route('/check_status', methods=['GET'])
def check_status():
    with open('status.json') as status_file:
        status = json.load(status_file)
    return jsonify(status)