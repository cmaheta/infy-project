from flask import Flask, Blueprint, session, jsonify,render_template, request, redirect, url_for
import subprocess
from util import create_upload_folder, allowed_file, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
import os
import pandas as pd



views = Blueprint(__name__, "views")


#@app.route('/run-script')
#def run_script():
#    result = subprocess.run(['python', 'python_script.py'], capture_output=True, text=True)
#    return jsonify({'output': result.stdout})

@views.route('/upload-file' , methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        create_upload_folder() 
        print('folder created')
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename);
            file_extension = os.path.splitext(file.filename)[1].lower()
            file.save(file_path)
            if file_extension == '.csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            jobs = df.iloc[:, 0].astype(str).tolist()
            session['jobs'] = jobs
            return redirect(url_for("views.select_jobs"))

    return render_template('upload.html')

@views.route('/select-jobs')
def select_jobs():
    jobs = session.get('jobs')
    return render_template('home.html', jobs=jobs)
