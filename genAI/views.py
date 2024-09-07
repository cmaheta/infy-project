from flask import Flask, Blueprint, session,flash, jsonify,render_template, request, redirect, url_for, send_from_directory
import subprocess
from util import run_bre_job_in_thread, check_system_resources_exhausted, create_folder, allowed_bre_file
from util import BRE_INPUT_FOLDER, BRE_OUTPUT_FOLDER
from werkzeug.utils import secure_filename
import os


views = Blueprint(__name__, "views")

@views.route('/bre-processes' , methods=['GET','POST'])
def bre_processes():
    return render_template('bre_processes.html')

@views.route('/bre-uploads' , methods=['GET','POST'])
def bre_uploads():
    if request.method == 'POST':
            if not check_system_resources_exhausted():
                flash("Can not upload your files. \n\n System resources exhausted. \n\n Please wait and try again.")
                return render_template('bre_processes.html')

            create_folder(BRE_INPUT_FOLDER) 
            
            if 'files[]' not in request.files:
                flash("No files selected.")

            files = request.files.getlist('files[]')
            uploaded_filenames = []

            for file in files:
                if file.filename == '':
                    continue 
                filename = secure_filename(file.filename)
                if allowed_bre_file(filename):
                    file.save(os.path.join(BRE_INPUT_FOLDER, filename))
                    uploaded_filenames.append(filename)
                
            if len(uploaded_filenames) > 0:
                run_bre_job_in_thread(uploaded_filenames)
                flash("Processing your files. Please check bre-downloads.")
                return render_template('bre_processes.html')
            else:
                flash("No file with .txt extension. Nothing to process.")

    return render_template('bre_processes.html')

@views.route('/bre-downloads', methods=['GET','POST'])
def bre_downloads():
    create_folder(BRE_OUTPUT_FOLDER) 
    files = os.listdir(BRE_OUTPUT_FOLDER)
    return render_template('bre_downloads.html', files=files)

@views.route('/bre-download-file/<filename>')
def bre_download_file(filename,  methods=['GET','POST']):
    return send_from_directory(BRE_OUTPUT_FOLDER, filename, as_attachment=True)

@views.route('/preview/<filename>')
def preview_file(filename):
    try:
        with open(os.path.join(BRE_OUTPUT_FOLDER, filename), 'r') as file:
            content = file.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)})    

@views.route('/')
def home():
    return render_template('home.html')