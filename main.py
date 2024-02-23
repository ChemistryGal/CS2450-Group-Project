from BusLogic import UVSimulator

def main():
    # Get user input
    # file = input("Hello! Welcome to UVSim. Please type the name of your txt file: ")
    
    # Create simulator object and load data into memory
    simulator = UVSimulator()
    simulator.load_program()
    
    # Run the program
    simulator.run_program()

if __name__ == "__main__":
    main()
