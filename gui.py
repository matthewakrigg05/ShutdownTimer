import tkinter as tk
from tkinter import messagebox, ttk
import program_options
from timer import Timer


class Gui:

    def __init__(self, root):
        self.countdown_label = None
        self.programs_options = ['Shutdown', 'Sleep', 'Log out', 'Restart', 'Lock Screen']

        self.root = root
        self.root.title("Shutdown Timer")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.build_gui()
        self.timer = Timer(
            update_callback=self.update_countdown,
            finish_callback=program_options.execute_shutdown
        )

    def build_gui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=15)

        self.options_label = tk.Label(frame, text="Please pick an option: ")
        self.options_label.grid(row=0, column=0, padx=10)
        self.options_cb = ttk.Combobox(frame, width=15, state="readonly")
        self.options_cb['values'] = self.programs_options
        self.options_cb.current(0)
        self.options_cb.grid(row=0, column=1, padx=10)

        self.desc_label = tk.Label(frame, text="Please enter a length of time: ")
        self.desc_label.grid(row=1, column=0, pady=10, columnspan=2)

        self.hours_label = tk.Label(frame, text="Hours")
        self.hours_label.grid(row=2, column=0, padx=5)
        self.hours_cb = ttk.Combobox(frame, width=5, state="readonly")
        self.hours_cb['values'] = [f"{i:02}" for i in range(24)]
        self.hours_cb.current(0)
        self.hours_cb.grid(row=3, column=0, padx=5)

        self.minutes_label = (tk.Label(frame, text="Minutes"))
        self.minutes_label.grid(row=2, column=1, padx=5)
        self.minutes_cb = ttk.Combobox(frame, width=5, state="readonly")
        self.minutes_cb['values'] = [f"{i:02}" for i in range(60)]
        self.minutes_cb.current(0)
        self.minutes_cb.grid(row=3, column=1, padx=5)

        self.schedule_button = (tk.Button(self.root, text="Schedule Shutdown", command=self.schedule_shutdown))
        self.schedule_button.pack(pady=5)

    def scheduled_gui(self):
        self.clear_gui()

        self.countdown_label = tk.Label(self.root, text="", font=("Helvetica", 12), fg="blue")
        self.countdown_label.pack(pady=10)

        self.cancel_button = (tk.Button(self.root, text="Cancel Shutdown", command=self.cancel))
        self.cancel_button.pack(pady=5)

    def cancel(self):
        self.timer.cancel()
        self.countdown_label.config(text="Shutdown cancelled.")
        messagebox.showinfo("Cancelled", "Scheduled shutdown has been cancelled.")

        self.clear_gui()
        self.build_gui()

    def schedule_shutdown(self):
        try:
            hours = int(self.hours_cb.get() or 0)
            minutes = int(self.minutes_cb.get() or 0)
            total_seconds = hours * 3600 + minutes * 60
            if total_seconds <= 0:
                raise ValueError

            messagebox.showinfo("Shutdown Scheduled", f"Shutdown in {hours}h {minutes}m.")
            self.scheduled_gui()
            self.timer.start(total_seconds)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid length of time.")

    def update_countdown(self, time_str): self.countdown_label.config(text=time_str)

    def clear_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
