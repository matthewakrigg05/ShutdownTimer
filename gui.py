import os
import tkinter as tk
from sys import platform
from tkinter import messagebox, ttk

from timer import Timer


class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Shutdown Timer")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.build_gui()
        self.timer = Timer(
            update_callback=self.update_countdown,
            finish_callback=self.execute_shutdown
        )

    def build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=15)

        tk.Label(frame, text="Hours").grid(row=0, column=0, padx=10)
        self.hours_cb = ttk.Combobox(frame, width=5, state="readonly")
        self.hours_cb['values'] = [f"{i:02}" for i in range(24)]
        self.hours_cb.current(0)
        self.hours_cb.grid(row=1, column=0, padx=10)

        tk.Label(frame, text="Minutes").grid(row=0, column=1, padx=10)
        self.minutes_cb = ttk.Combobox(frame, width=5, state="readonly")
        self.minutes_cb['values'] = [f"{i:02}" for i in range(60)]
        self.minutes_cb.current(0)
        self.minutes_cb.grid(row=1, column=1, padx=10)

        self.countdown_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="blue")
        self.countdown_label.pack(pady=10)

        tk.Button(self.root, text="Schedule Shutdown", command=self.schedule_shutdown).pack(pady=5)
        tk.Button(self.root, text="Cancel Shutdown", command=self.cancel_shutdown).pack(pady=5)

    def schedule_shutdown(self):
        try:
            hours = int(self.hours_entry.get() or 0)
            minutes = int(self.minutes_entry.get() or 0)
            total_seconds = hours * 3600 + minutes * 60
            if total_seconds <= 0:
                raise ValueError
            self.timer.start(total_seconds)
            messagebox.showinfo("Shutdown Scheduled", f"Shutdown in {hours}h {minutes}m.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers.")

    def update_countdown(self, time_str):
        self.countdown_label.config(text=time_str)

    def execute_shutdown(self):
        system = platform.system()
        if system == "Windows":
            os.system("shutdown /s /t 1")
        elif system == "Linux" or system == "Darwin":
            os.system("shutdown -h now")
        else:
            messagebox.showerror("Unsupported OS", f"Shutdown not supported on {system}")

    def cancel_shutdown(self):
        self.timer.cancel()
        self.countdown_label.config(text="Shutdown cancelled.")
        messagebox.showinfo("Cancelled", "Scheduled shutdown has been cancelled.")
