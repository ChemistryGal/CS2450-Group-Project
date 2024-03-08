# controller.py
import tkinter as tk

class Controller:
    def __init__(self, model):
        self.model = model

    def show_input_window(self):
        # Create a new Tkinter window for user input
        input_window = tk.Tk()
        input_window.title("User Input")

        # Entry widget for user input
        entry = tk.Entry(input_window)
        entry.pack(pady=10)

        # Button to submit user input
        submit_button = tk.Button(input_window, text="Submit", command=lambda: self.process_user_input(entry.get(), input_window))
        submit_button.pack(pady=10)

        input_window.mainloop()

    def process_user_input(self, user_input, input_window):
        # Process the user input (you can replace this with your own logic)
        if user_input:
            print("Controller received user input:", user_input)
        else:
            print("Controller received no input.")

        # Close the input window
        input_window.destroy()
