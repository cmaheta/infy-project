from flask import Flask, Blueprint,session, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from python_script import run_bre_job_in_thread, run_fe_job_in_thread
import threading
import asyncio
import os
import psutil
import uuid

BRE_INPUT_FOLDER = 'bre_inputs/'
BRE_OUTPUT_FOLDER = 'bre_outputs/'
FE_INPUT_FOLDER = 'fe_inputs/'
FE_OUTPUT_FOLDER = 'fe_outputs/'

ALLOWED_EXTENSIONS = {'.txt'}


def run_job_in_thread(uploaded_filenames, unique_id):
    def target_bre():
        result = asyncio.run(run_bre_job_in_thread(uploaded_filenames, unique_id))
        print(result)

    def target_fe():
        result = asyncio.run(run_fe_job_in_thread(uploaded_filenames, unique_id))
        print(result)
        
    flag_value = session.get('flag_value', '')
    print(f"Flag value received: {flag_value}")

    if flag_value == 'bre':
        print("bre job is running")
        thread = threading.Thread(target=target_bre)
        thread.start()

    if flag_value == 'fe':
        print("fe job is running")
        thread = threading.Thread(target=target_fe)
        thread.start()
    
def check_system_resources_exhausted():
    memory_threshold = 80  # in percentage
    cpu_threshold = 80     # in percentage

    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"memory usage is {memory_usage}")
    print(f"cpu usage is {cpu_usage}")
    if memory_usage > memory_threshold or cpu_usage > cpu_threshold:
        return False
    return True

# Helper function to check allowed file extensions
def allowed_file(filename):
    file_extension = os.path.splitext(filename)[1].lower() 
    print(file_extension)
    return file_extension.lower() in ALLOWED_EXTENSIONS

def create_folders():
      if not os.path.exists(BRE_INPUT_FOLDER):
            os.makedirs(BRE_INPUT_FOLDER)

      if not os.path.exists(FE_INPUT_FOLDER):
            os.makedirs(FE_INPUT_FOLDER)   

      if not os.path.exists(BRE_OUTPUT_FOLDER):
            os.makedirs(BRE_OUTPUT_FOLDER)

      if not os.path.exists(FE_OUTPUT_FOLDER):
            os.makedirs(FE_OUTPUT_FOLDER)         

def list_download_files():
    return os.listdir(get_output_folder())

def process_files(files):
    uploaded_filenames = []
    
    for file in files:
        if file.filename == '':
            continue 
        filename = secure_filename(file.filename)
        if allowed_file(filename):
            file.save(os.path.join(get_input_folder(), filename))
            uploaded_filenames.append(filename)

    run_jobs(uploaded_filenames)

def run_jobs(uploaded_filenames):
    if len(uploaded_filenames) > 0:
        unique_id = uuid.uuid4()
        run_job_in_thread(uploaded_filenames, unique_id)
        flash(f"Processing your files. Your unique jobID is {unique_id}.")
        flash(f"Please check {get_download_text()}")
    else:
        flash("No file with .txt extension. Nothing to process.")

def get_output_folder():
    flag_value = session.get('flag_value', '')
    print(f"Flag value received: {flag_value}")

    if flag_value == 'bre':
        return BRE_OUTPUT_FOLDER
    
    if flag_value == 'fe':
        return FE_OUTPUT_FOLDER

def get_input_folder():
    flag_value = session.get('flag_value', '')
    print(f"Flag value received: {flag_value}")

    if flag_value == 'bre':
        return BRE_INPUT_FOLDER

    if flag_value == 'fe':
        return FE_INPUT_FOLDER

def get_download_text():
    flag_value = session.get('flag_value', '')
    print(f"Flag value received: {flag_value}")

    if flag_value == 'bre':
        return 'BRE-DOWNLOADS'

    if flag_value == 'fe':
        return 'FE-DOWNLOADS'
