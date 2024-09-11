from flask import Flask, Blueprint,session, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from python_script import run_bre_job_in_thread, run_fe_job_in_thread
import threading
import asyncio
import os
import psutil
import uuid
import json

BRE_INPUT_FOLDER = 'bre_inputs/'
BRE_OUTPUT_FOLDER = 'bre_outputs/'
FE_INPUT_FOLDER = 'fe_inputs/'
FE_OUTPUT_FOLDER = 'fe_outputs/'

ALLOWED_EXTENSIONS = {'.txt', '.docx'}


def run_job_in_thread(uploaded_filenames, process_type):
    def target_run(process_type):

        status = {"progress": 25, "message": "Processing files..."}

        with open('status.json', 'w') as status_file:
            json.dump(status, status_file)

        if process_type == 'bre':
            print('bre job is running')
            result = asyncio.run(run_bre_job_in_thread(uploaded_filenames))

        if process_type == 'fe':
            print('fe job is running') 
            result = asyncio.run(run_fe_job_in_thread(uploaded_filenames))

        status = {"progress": 100, "message": "Process complete."}
    
        with open('status.json', 'w') as status_file:
            json.dump(status, status_file)

        print(result)
        
    thread = threading.Thread(target=lambda: target_run(process_type))
    thread.start()

# Helper function to check allowed file extensions
def allowed_file(filename):
    file_extension = os.path.splitext(filename)[1].lower() 
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

def process_files(files, process_type):
    uploaded_filenames = []
    
    for file in files:
        if file.filename == '':
            continue 
        filename = secure_filename(file.filename)
        if allowed_file(filename):
            file.save(os.path.join(get_input_folder(), filename))
            uploaded_filenames.append(filename)

    run_job_in_thread(uploaded_filenames, process_type)

def get_output_folder():
    process_type = session.get('process_type', '')
    print(f"Flag value received: {process_type}")

    if process_type == 'bre':
        return BRE_OUTPUT_FOLDER
    
    if process_type == 'fe':
        return FE_OUTPUT_FOLDER

def get_input_folder():
    process_type = session.get('process_type', '')
    print(f"Flag value received: {process_type}")

    if process_type == 'bre':
        return BRE_INPUT_FOLDER

    if process_type == 'fe':
        return FE_INPUT_FOLDER
