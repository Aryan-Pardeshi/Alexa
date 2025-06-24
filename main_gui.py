import tkinter as tk
from tkinter import Canvas, Label, Entry, StringVar
import threading
import time
import speech_recognition as sr
from playsound import playsound
from main import processCommand
import os

class AlexaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa GUI")
        self.root.configure(bg="#111")
        self.root.geometry("400x500")
        self.is_listening = False
        self.is_speaking = False
        self.ring_radius = 80
        self.ring_width = 14  # Thicker outline
        self.ring_color = "#3A5EFF"
        self.animation_running = False

        self.canvas = Canvas(self.root, width=250, height=250, bg="#111", highlightthickness=0)
        self.canvas.pack(pady=30)
        self.ring = self.canvas.create_oval(
            35, 35, 215, 215, outline=self.ring_color, width=self.ring_width
        )

        self.label = Label(
            self.root, text="Hello i am Alexa,\nSay \"Alexa\" to Activate!", fg="white", bg="#111", font=("Arial", 13)
        )
        self.label.pack(pady=10)

        self.output_var = StringVar()
        self.output_entry = Entry(self.root, textvariable=self.output_var, font=("Arial", 12), width=30, bg="#222", fg="white", bd=0, justify="center")
        self.output_entry.pack(pady=20)

        self.status_var = StringVar()
        # self.status_label = Label(self.root, textvariable=self.status_var, fg="red", bg="#111", font=("Arial", 10))
        # self.status_label.pack(pady=5)

        # Add Stop button for clean exit
        self.stop_button = tk.Button(self.root, text="Stop", command=self.clean_exit, bg="#d9534f", fg="white", font=("Arial", 11), relief="flat")
        self.stop_button.pack(pady=10)

        # Start listening after window is visible
        # self.root.after(500, self.start_listen_thread)  # DISABLED: Avoid double mic usage
        self.root.after(500, self.listen_for_wake_word)  # Use only one listener

    def speak_output(self, text):
        self.output_var.set(text)
        self.root.update_idletasks()

    def start_listen_thread(self):
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()

    def listen_loop(self):
        pass  # Disabled to avoid double microphone usage

    def animate_ring(self):
        self.animation_running = True
        grow = True
        min_radius = 80
        max_radius = 95
        step = 1  # Smaller step for smoother animation
        while self.is_speaking:
            for _ in range((max_radius - min_radius) // step):
                if not self.is_speaking:
                    break
                if grow:
                    self.ring_radius = min(self.ring_radius + step, max_radius)
                else:
                    self.ring_radius = max(self.ring_radius - step, min_radius)
                self.update_ring()
                self.root.update_idletasks()
                time.sleep(0.03)  # Smoother, less aggressive
            grow = not grow
        self.ring_radius = min_radius
        self.update_ring()
        self.animation_running = False

    def update_ring(self):
        x0 = 125 - self.ring_radius
        y0 = 125 - self.ring_radius
        x1 = 125 + self.ring_radius
        y1 = 125 + self.ring_radius
        self.canvas.coords(self.ring, x0, y0, x1, y1)

    def listen_for_wake_word(self):
        r = sr.Recognizer()
        def listen_loop():
            while True:
                try:
                    with sr.Microphone() as source:
                        audio = r.listen(source, timeout=2, phrase_time_limit=1)
                        word = r.recognize_google(audio)
                    if word.lower() == "alexa":
                        if os.path.exists("wake.mp3"):
                            playsound("wake.mp3")
                        self.output_var.set("Alexa Active... Listening...")
                        self.is_speaking = True
                        threading.Thread(target=self.animate_ring, daemon=True).start()
                        with sr.Microphone() as source:
                            audio = r.listen(source, timeout=5, phrase_time_limit=15)
                            command = r.recognize_google(audio)
                        if os.path.exists("end.mp3"):
                            playsound("end.mp3")
                        self.output_var.set(f"You said: {command}")
                        self.speak_and_process(command)
                except Exception as e:
                    # self.status_var.set(f"Mic/Recognition Error: {e}")
                    time.sleep(2)
        threading.Thread(target=listen_loop, daemon=True).start()

    def speak_and_process(self, command):
        def run():
            processCommand(command)
            self.is_speaking = False
        threading.Thread(target=run, daemon=True).start()

    def clean_exit(self):
        self.root.destroy()
        os._exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlexaGUI(root)
    root.mainloop()
