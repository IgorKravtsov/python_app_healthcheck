import tkinter as tk
from datetime import datetime
from tkinter import filedialog
import psutil
import threading
import os
import time

from HealthChecker.healthChecker import HealthChecker


def is_program_running(program_path):
    process_name = os.path.basename(program_path)
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False


def select_program():
    file_path = filedialog.askopenfilename()
    if file_path:
        health_checker.set_program_to_check(file_path)
        program_path.set(file_path)


def check_program_state():
    while True:
        now = datetime.now()
        if health_checker.program_path:
            if is_program_running(health_checker.program_path):
                message = f"[{now.strftime('%H:%M:%S')}] Running\n"
                health_checker.append_to_program_state_history(message)
            else:
                health_checker.start_program()
                message = f"[{now.strftime('%H:%M:%S')}] Not Running\n"
                health_checker.append_to_program_state_history(message)

            program_state.set(','.join(health_checker.program_state_history))
        time.sleep(3)


# Create the main GUI window
root = tk.Tk()
root.title("Program State Checker")
root.geometry("700x550")

# Variables to store the program path and its state
program_path = tk.StringVar()
program_state = tk.StringVar()

# GUI elements
program_label = tk.Label(root, text="Selected Program:")
program_label.pack()

program_entry = tk.Entry(root, textvariable=program_path, width=30)
program_entry.pack()

select_button = tk.Button(root, text="Select Program", command=select_program)
select_button.pack()

state_label = tk.Label(root, text="Program State:")
state_label.pack()

state_display = tk.Label(root, textvariable=program_state)
state_display.pack()

health_checker = HealthChecker(program_path.get())

# Start the thread for periodic checking
state_check_thread = threading.Thread(target=check_program_state)
state_check_thread.daemon = True
state_check_thread.start()

root.mainloop()