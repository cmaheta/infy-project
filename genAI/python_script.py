from tkinter import messagebox
import time
import os

async def run_bre_job_in_thread(selected_files, unique_id):
    BRE_OUTPUT_FOLDER = 'bre_outputs/'
    BRE_INPUT_FOLDER = 'bre_inputs/'

    for file_name in selected_files:
        file_input_path = os.path.join(BRE_INPUT_FOLDER, file_name)
        file_output_path = os.path.join(BRE_OUTPUT_FOLDER, str(unique_id)+"_"+file_name)
        with open(file_input_path, 'r') as input_file:
            file_contents = input_file.read()
        with open(file_output_path, 'w') as output_file:
            output_file.write(file_contents)  

    print("sleep started")   
    time.sleep(15)
    print("sleep ended")    
    return f"Files from the jobs run created at xyz location."

async def run_fe_job_in_thread(selected_files, unique_id):
    FE_OUTPUT_FOLDER = 'fe_outputs/'
    FE_INPUT_FOLDER = 'fe_inputs/'

    for file_name in selected_files:
        file_input_path = os.path.join(FE_INPUT_FOLDER, file_name)
        file_output_path = os.path.join(FE_OUTPUT_FOLDER, str(unique_id)+"_"+file_name)
        with open(file_input_path, 'r') as input_file:
            file_contents = input_file.read()
        with open(file_output_path, 'w') as output_file:
            output_file.write(file_contents)  

    print("sleep started")   
    time.sleep(15)
    print("sleep ended")    
    return f"Files from the jobs run created at xyz location."    
    