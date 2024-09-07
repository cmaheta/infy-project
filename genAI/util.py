from flask import Flask, Blueprint,session, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from python_script import run_job_in_thread;
import threading
import asyncio
import os
import psutil

BRE_INPUT_FOLDER = 'bre_inputs/'
BRE_OUTPUT_FOLDER = 'bre_outputs/'
ALLOWED_EXTENSIONS = {'.txt'}

def run_bre_job_in_thread(uploaded_filenames):
    def target():
        result = asyncio.run(run_job_in_thread(uploaded_filenames))
        print(result)

    thread = threading.Thread(target=target)
    thread.start()
    return thread    
    
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
def allowed_bre_file(filename):
    file_extension = os.path.splitext(filename)[1].lower() 
    print(file_extension)
    return file_extension.lower() in ALLOWED_EXTENSIONS

def create_folder(FOLDER_PATH):
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

# Route for handling the upload page

