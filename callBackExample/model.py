# backend.py
import time

class Model:
    def __init__(self, controller):
        self.controller = controller

    def start_execution(self):
        # Execute some initialization tasks
        print("Backend is starting...")
        
        # Wait for a few seconds (you can replace this with your own initialization logic)
        self.controller.show_input_window()
