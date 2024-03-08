from view import AppView
from controller import Controller
from model import Model
import tkinter as tk


# Create the main Tkinter window and MVC components
if __name__ == "__main__":
    root = tk.Tk()
    controller = Controller(None)  # The controller will be set later
    view = AppView(root, controller)
    controller.model = Model(controller)  # Set the backend for the controller

    # Run the Tkinter event loop
    root.mainloop()



"""
Notes on how to structure the application

UVsimulator class must contain an instance of the model
Model Class must contain a shared instance of the UVsimulator
View class must contain the same shared instance of the UVsimulator

new classes to add
Classes.py break them into a CPU class that handles operations and Memory class that handles the data
-CPU
-Memory


"""
