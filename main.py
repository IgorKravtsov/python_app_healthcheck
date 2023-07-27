from threading import Thread
import psutil
import subprocess
from sys import platform

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from HealthChecker.healthChecker import HealthChecker


def start_program(program_path: str):
    try:
        subprocess.call(program_path, shell=platform == 'darwin')
        print(f"{program_path} started successfully.")
    except FileNotFoundError:
        print(f"Error: {program_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_all_processes():
    all_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'exe', 'status']):
        try:
            process_info = proc.info
            all_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return all_processes


def is_program_running(program_name: str):
    for proc in psutil.process_iter(['exe']):
        # print(proc.info)
        if proc.info['exe'] == program_name:
            return True
    return True

def select_file():
    file = fd.askopenfilename(
        title='Выбрать файл',
        initialdir='/',
    )
    return file

if __name__ == "__main__":
    program_to_check = "/Applications/AnyDesk.app/Contents/MacOS/AnyDesk"
    root = tk.Tk()

    root.title('Health checker')
    root.resizable(False, False)
    root.geometry('300x150')

    open_button = ttk.Button(
        root,
        text='Выберите программу',
        command=select_file
    )

    health_checker = HealthChecker(program_to_check)

    thread = Thread(target=health_checker.start_main_loop)
    thread.start()

    open_button.pack(expand=True)

    root.mainloop()


