from flask import Flask, Blueprint, session,flash, jsonify,render_template, request, redirect, url_for, Response
import subprocess
from util import run_jobs_in_thread, check_system_resources_exhausted, create_upload_folder, allowed_bre_file, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from python_script import run_jobs;
import os


views = Blueprint(__name__, "views")

@views.route('/upload-file' , methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
            if not check_system_resources_exhausted():
                flash("Can not upload your files. \n\n System resources exhausted. \n\n Please wait and try again")
                return render_template('upload_folders.html')

            create_upload_folder() 
            
            if 'files[]' not in request.files:
                flash("No files selected.")

            files = request.files.getlist('files[]')
            uploaded_filenames = []

            for file in files:
                if file.filename == '':
                    continue 
                filename = secure_filename(file.filename)
                if allowed_bre_file(filename):
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    uploaded_filenames.append(filename)
                
            if len(uploaded_filenames) > 0:
                run_jobs_in_thread(files)
                flash("Processing your files. Please check bre-downloads.")
                return render_template('bre_home.html')
            else:
                flash("No file with .txt extension. Nothing to process.")

    return render_template('bre_home.html')