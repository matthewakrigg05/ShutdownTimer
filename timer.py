import threading
import time


class Timer:
    def __init__(self, update_callback, finish_callback):
        self.update_callback = update_callback
        self.finish_callback = finish_callback
        self.cancel_event = threading.Event()
        self.thread = None

    def start(self, total_seconds):
        if total_seconds <= 0:
            raise ValueError("Total seconds must be positive.")

        self.cancel_event.clear()

        def run():
            remaining = total_seconds
            while remaining > 0:
                if self.cancel_event.is_set():
                    return
                h, rem = divmod(remaining, 3600)
                m, s = divmod(rem, 60)
                self.update_callback(f"Time remaining: {h:02d}:{m:02d}:{s:02d}")
                time.sleep(1)
                remaining -= 1

            if not self.cancel_event.is_set():
                self.finish_callback()

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def cancel(self):
        self.cancel_event.set()