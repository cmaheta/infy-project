from flask import Flask, Blueprint,session, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from python_script import run_jobs;
import threading
import asyncio
import os

UPLOAD_FOLDER = 'bre_uploads/'
ALLOWED_EXTENSIONS = {'.txt'}


# Helper function to check allowed file extensions
def allowed_bre_file(filename):
    file_extension = os.path.splitext(filename)[1].lower() 
    print(file_extension)
    return file_extension.lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# Route for handling the upload page

