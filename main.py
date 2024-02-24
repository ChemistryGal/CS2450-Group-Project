from BusLogic import UVSimulator
from ui_accumulator import tkinterApp

def main():
    # Get user input
    # file = input("Hello! Welcome to UVSim. Please type the name of your txt file: ")
    
    # Create simulator object and load data into memory
    simulator = UVSimulator()
    # Driver Code - move and import these into the main function to run the application.
    app = tkinterApp(simulator)
    app.mainloop()

if __name__ == "__main__":
    main()
    # Create storage obj and load data into memory
    storage = Storage()
    storage.load_memory(file)
    execute_loop(storage)

main()
