import subprocess
import time
from datetime import datetime
from sys import platform
import psutil

from Logger import Logger


class HealthChecker:
    def __init__(self, program_path_to_check, sleep_interval=3, logger=Logger.Logger):
        self.program_path = program_path_to_check.strip()
        self.sleep_interval = sleep_interval
        self.logger = logger
        self.current_status = ""
        self.program_state_history = []

    def is_program_running(self):
        for proc in psutil.process_iter(['exe']):
            if proc.info['exe'] and proc.info['exe'] in self.program_path:
                return True
        return False

    def append_to_program_state_history(self, state: str):
        self.program_state_history.append(state)

    def start_program(self):
        try:
            subprocess.call(self.program_path, shell=platform == 'darwin')
            message = f"{self.program_path} запускается."
            self.logger.log(message)
            self.append_to_program_state_history(message)
        except FileNotFoundError:
            self.logger.log(f"Ошибка: {self.program_path} не найдена.")
        except Exception as e:
            self.logger.log(f"An error occurred: {e}")

    @staticmethod
    def print_all_processes():
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'status']):
            print(proc.info)

    def get_current_status(self):
        return self.current_status

    def set_program_to_check(self, program_path: str):
        self.program_path = program_path

    def start_main_loop(self):
        # self.print_all_processes()
        try:
            while True:
                now = datetime.now()
                if self.is_program_running():
                    message = f"[{now.strftime('%H:%M:%S')}] {self.program_path} запущена."
                    self.current_status = message
                else:
                    message = f"[{now.strftime('%H:%M:%S')}] {self.program_path} не запущена."
                    self.current_status = message
                    self.start_program()

                self.append_to_program_state_history(message)
                self.logger.log(self.current_status)
                time.sleep(self.sleep_interval)

        except KeyboardInterrupt:
            self.logger.log("Программа остановлена")