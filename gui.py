import tkinter as tk
from tkinter import messagebox, ttk
from program_options import OptionHandler
from timer import Timer


# noinspection PyAttributeOutsideInit
class Gui:

    def __init__(self, root):
        self.programs_options = ['Shutdown', 'Sleep', 'Log Out', 'Restart', 'Lock Screen']

        self.root = root
        self.root.title("Shutdown Timer")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.build_gui()

    def build_gui(self):
        self.root.configure(bg="#f0f0f0")  # Light background

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=20)

        title = tk.Label(frame, text="System Action Scheduler", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.options_label = tk.Label(frame, text="Select action:", bg="#f0f0f0")
        self.options_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.options_cb = ttk.Combobox(frame, width=17, state="readonly", values=self.programs_options)
        self.options_cb.current(0)
        self.options_cb.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        self.desc_label = tk.Label(frame, text="Delay duration:", bg="#f0f0f0")
        self.desc_label.grid(row=2, column=0, sticky="e", padx=5, pady=(10, 5))

        time_frame = tk.Frame(frame, bg="#f0f0f0")
        time_frame.grid(row=2, column=1, sticky="w", pady=(10, 5))

        self.hours_cb = ttk.Combobox(time_frame, width=5, state="readonly", values=[f"{i:02}" for i in range(24)])
        self.hours_cb.current(0)
        self.hours_cb.grid(row=0, column=0, padx=(0, 5))

        hours_label = tk.Label(time_frame, text="h", bg="#f0f0f0")
        hours_label.grid(row=0, column=1)

        self.minutes_cb = ttk.Combobox(time_frame, width=5, state="readonly", values=['00', '15', '30', '45'])
        self.minutes_cb.current(0)
        self.minutes_cb.grid(row=0, column=2, padx=(10, 5))

        minutes_label = tk.Label(time_frame, text="m", bg="#f0f0f0")
        minutes_label.grid(row=0, column=3)

        self.schedule_button = tk.Button(self.root, text="Schedule Action", command=self.schedule, bg="#4CAF50",
                                         fg="white", font=("Helvetica", 10, "bold"))
        self.schedule_button.pack(pady=15)

    def scheduled_gui(self):
        self.clear_gui()

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=30)

        title = tk.Label(frame, text=f"{self.option_scheduled} Scheduled", font=("Helvetica", 14, "bold"), fg="blue",
                         bg="#f0f0f0")
        title.pack(pady=(0, 10))

        self.countdown_label = tk.Label(frame, text="", font=("Helvetica", 12), fg="blue", bg="#f0f0f0")
        self.countdown_label.pack(pady=5)

        self.cancel_button = tk.Button(
            self.root,
            text=f"Cancel {self.option_scheduled}",
            command=self.cancel,
            bg="#d9534f",
            fg="white",
            font=("Helvetica", 10, "bold"),
            padx=10,
            pady=5
        )
        self.cancel_button.pack(pady=10)

    def cancel(self):
        self.timer.cancel()
        self.countdown_label.config(text=f"{self.option_scheduled} cancelled.")
        messagebox.showinfo("Cancelled", f"Scheduled {self.option_scheduled} has been cancelled.")

        self.clear_gui()
        self.build_gui()

    def schedule(self):
        self.option_scheduled = self.options_cb.get()
        try:
            hours = int(self.hours_cb.get() or 0)
            minutes = int(self.minutes_cb.get() or 0)
            total_seconds = hours * 3600 + minutes * 60

            if total_seconds <= 0:
                raise ValueError

            messagebox.showinfo(f"{self.option_scheduled} Scheduled", f"{self.option_scheduled} in {hours}h {minutes}m.")

            self.scheduled_gui()

            self.option_handler = OptionHandler(self.option_scheduled)
            self.option_handler.check_options()
            self.timer = Timer(
                update_callback=self.update_countdown,
                finish_callback=self.option_handler.function_needed
            )

            self.timer.start(total_seconds)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid length of time.")

    def update_countdown(self, time_str): self.countdown_label.config(text=time_str)

    def clear_gui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
