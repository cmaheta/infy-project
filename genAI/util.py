from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import pandas as pd

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.csv'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    file_extension = os.path.splitext(filename)[1].lower() 
    print(file_extension)
    return file_extension.lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# Route for handling the upload page

