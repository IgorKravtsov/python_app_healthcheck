import psutil
import subprocess
import time


def start_program(program_path):
    try:
        subprocess.Popen(program_path)
        print(f"{program_path} started successfully.")
    except FileNotFoundError:
        print(f"Error: {program_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_all_processes():
    all_processes = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_info = proc.info
            all_processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return all_processes


def is_program_running(program_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == program_name:
            return True
    return False


if __name__ == "__main__":
    program_to_check = "Slack.app"
    try:
        while True:
            if is_program_running(program_to_check):
                print(f"{program_to_check} is running.")
            else:
                print(f"{program_to_check} is not running.")
                start_program(program_to_check)

            time.sleep(3)  # Wait for 3 seconds before checking again

    except KeyboardInterrupt:
        print("PROGRAM STOPPED!")
