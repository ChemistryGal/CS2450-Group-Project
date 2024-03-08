# view.py
import tkinter as tk

class AppView:
    def __init__(self, root, controller):
        # Create the main Tkinter window
        self.root = root
        self.root.title("MVC App")

        # Create a button to trigger the backend execution
        button = tk.Button(self.root, text="Start Backend", command=self.start_backend)
        button.pack(pady=20)

        # Set the controller
        self.controller = controller

    def start_backend(self):
        # Initialize the backend and start its execution
        backend = self.controller.model
        backend.start_execution()