from flask import Flask, Blueprint,session, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from python_script import run_jobs;
import threading
import asyncio
import os
import psutil

UPLOAD_FOLDER = 'bre_uploads/'
ALLOWED_EXTENSIONS = {'.txt'}

def run_jobs_in_thread(items):
    def target():
        result = asyncio.run(run_jobs(items))
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

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# Route for handling the upload page

