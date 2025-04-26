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
        if self.operating_system == "Windows":
            os.system("shutdown -l")
        elif self.operating_system == "Linux":
            os.system("gnome-session-quit --logout --no-prompt")  # works for GNOME desktops
        elif self.operating_system == "Darwin":
            os.system('osascript -e \'tell application "System Events" to log out\'')
        else:
            messagebox.showerror("Unsupported Operating System", f"Logout not supported on {self.operating_system}")

    def execute_sleep(self):
        if self.operating_system == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif self.operating_system == "Linux":
            os.system("systemctl suspend")
        elif self.operating_system == "Darwin":
            os.system('pmset sleepnow')
        else:
            messagebox.showerror("Unsupported Operating System", f"Sleep not supported on {self.operating_system}")

    def execute_restart(self):
        if self.operating_system == "Windows":
            os.system("shutdown -r -t 1")
        elif self.operating_system == "Linux" or self.operating_system == "Darwin":
            os.system("shutdown -r now")
        else:
            messagebox.showerror("Unsupported Operating System", f"Restart not supported on {self.operating_system}")

    def execute_lockscreen(self):
        if self.operating_system == "Windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif self.operating_system == "Linux":
            os.system("gnome-screensaver-command -l")  # works if gnome-screensaver installed
        elif self.operating_system == "Darwin":
            os.system('/System/Library/CoreServices/"Menu Extras"/User.menu/Contents/Resources/CGSession -suspend')
        else:
            messagebox.showerror("Unsupported Operating System",
                                 f"Lock screen not supported on {self.operating_system}")
