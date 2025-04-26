import os
import platform
from tkinter import messagebox


class OptionHandler:
    def __init__(self, option):
        self.option = option
        self.operating_system = platform.system()
        self.function_needed = None

    def check_options(self):
        match self.option:
            case "Shutdown":
                self.function_needed = self.execute_shutdown
            case "Sleep":
                self.function_needed = self.execute_sleep
            case "Restart":
                self.function_needed = self.execute_restart
            case "Log Out":
                self.function_needed = self.execute_logout
            case "Lock Screen":
                self.function_needed = self.execute_lockscreen

    def execute_shutdown(self):
        if self.operating_system == "Windows":
            os.system("shutdown -s -t 1")
        elif self.operating_system == "Linux" or self.operating_system == "Darwin":
            os.system("shutdown -h now")
        else:
            messagebox.showerror("Unsupported Operating System", f"Shutdown not supported on {self.operating_system}")

    def execute_logout(self):
        messagebox.showinfo("Unsupported Operating System", f"Logged Out!")

    def execute_sleep(self):
        messagebox.showinfo("Unsupported Operating System", f"Sleeping!")

    def execute_restart(self):
        messagebox.showinfo("Unsupported Operating System", f"Restarted!")

    def execute_lockscreen(self):
        messagebox.showinfo("Unsupported Operating System", f"Locked Screen!")
