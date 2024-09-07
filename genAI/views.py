from flask import Flask, Blueprint, session,flash, jsonify,render_template, request, redirect, url_for
import subprocess
from util import create_upload_folder, allowed_bre_file, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from python_script import run_jobs;
import os
import pandas as pd

views = Blueprint(__name__, "views")

@views.route('/upload-file' , methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
            create_upload_folder() 
            if 'files[]' not in request.files:
                flash("No files selected")

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
                result = run_jobs(files)
                flash(result)
                return render_template('upload_folders.html')
            else:
                flash("No file with .txt extension. Nothing to process")

    return render_template('upload_folders.html')
        