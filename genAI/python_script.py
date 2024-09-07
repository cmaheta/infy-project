from tkinter import messagebox
import time

def run_jobs(selected_files):
    for file in selected_files:
        print(file.filename)
    time.sleep(60)
    return f"Files from the jobs run created at xyz location."
    