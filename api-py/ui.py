import tkinter as tk
from python_script import run_jobs;
import asyncio
from dotenv import load_dotenv
import time
import threading
import os

load_dotenv()

def run_jobs_in_thread(items):
    def target():
        # This function will be executed in the thread
        result = asyncio.run(run_jobs(items))
        print(result)  # You can handle the result here
        label.config(text=f"Jobs: {', '.join(items)} finished running successfully. \n {result}")
        button.config(state=tk.NORMAL)

    # Create and start the thread
    thread = threading.Thread(target=target)
    thread.start()
    return thread

# Function to display selected items
def btn_click():
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(i) for i in selected_indices]
    listbox.selection_clear(0, tk.END)
    # Disable the button
    button.config(state=tk.DISABLED)
    label.config(text=f"Jobs: {', '.join(selected_items)} running...")
    run_jobs_in_thread(selected_items)

# Create the main window
root = tk.Tk()
root.title("Gen AI Jobs Dashboard")

# Create a Listbox widget with multiple selection mode
listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10, width=40)
listbox.pack(padx=10, pady=10)

# Add items to the Listbox
items_str = os.getenv('ITEMS', '')
print(items_str)
items = [item.strip() for item in items_str.split(',') if item.strip()]
for item in items:
    listbox.insert(tk.END, item)

# Create a Button to show selected items
button = tk.Button(root, text="Run Jobs", command=btn_click)
button.pack(pady=10)
label = tk.Label(root, text="", padx=10, pady=10)
label.pack()
# Start the Tkinter event loop
root.mainloop()
