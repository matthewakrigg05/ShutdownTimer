import os
import platform
from tkinter import messagebox


def execute_shutdown():
    system = platform.system()
    if system == "Windows":
        os.system("shutdown -s -t 1")
    elif system == "Linux" or system == "Darwin":
        os.system("shutdown -h now")
    else:
        messagebox.showerror("Unsupported Operating System", f"Shutdown not supported on {system}")


