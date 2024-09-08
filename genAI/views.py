from flask import Flask, Blueprint, session,flash, jsonify,render_template, request, redirect, url_for, send_from_directory
from util import check_system_resources_exhausted, create_folders, process_files, get_output_folder, list_download_files
import os

views = Blueprint(__name__, "views")

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/ai-processes' , methods=['GET','POST'])
def ai_processes():
    flag_value = request.form.get('flag')
    print(f"Flag value received: {flag_value}")
    session['flag_value'] = flag_value

    if request.method == 'POST':
        return render_template('ai_processes.html',flag_value=flag_value)
    else:
        return redirect(url_for("views.home"))

@views.route('/ai-uploads' , methods=['GET','POST'])
def ai_uploads():
    if request.method == 'POST':
        flag_value = session.get('flag_value', '')
        if not check_system_resources_exhausted():
            flash("Can not upload your files. \n\n System resources exhausted. \n\n Please wait and try again.")
            return render_template('ai_processes.html')
            
        if 'files[]' not in request.files:
            flash("No files selected.")
        else:
            files = request.files.getlist('files[]')
            create_folders()
            process_files(files)
        
        return render_template('ai_processes.html', flag_value=flag_value)
    else:
        return redirect(url_for("views.home"))    

@views.route('/ai-downloads', methods=['GET','POST'])
def ai_downloads():
    flag_value = request.form.get('flag')
    print(f"Flag value received: {flag_value}")
    session['flag_value'] = flag_value

    if request.method == 'POST':
        create_folders() 
        files = list_download_files()
        return render_template('ai_downloads.html', files=files, flag_value=flag_value)
    else:
        return redirect(url_for("views.home"))    

@views.route('/ai-download-file/<filename>')
def ai_download_file(filename,  methods=['POST']):
    return send_from_directory(get_output_folder(), filename, as_attachment=True)

@views.route('/preview/<filename>')
def preview_file(filename):
    try:
        with open(os.path.join(get_output_folder(), filename), 'r') as file:
            content = file.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)})    

@views.route('/delete-file/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        # Construct full file path
        file_path = os.path.join(get_output_folder(), filename)

        # Check if file exists
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": f"{filename} deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    