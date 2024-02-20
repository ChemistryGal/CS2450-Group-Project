from Classes import *


def main():
    # Get user input
    file = input(
        "Hello! Welcome to UVSim. Please type the name of your txt file: ")
    # Create storage obj and load data into memory
    storage = Storage()
    storage.load_memory(file)
    # Validate the memory that was loaded. Throw an error if there is an incorrect instruction - throw an error message to the console.

    while storage.loc <= len(storage.memory):
        instr = storage.memory[storage.loc]
        control = [40, 41, 42, 43]
        ls = [20, 21]
        arith = [30, 31, 32, 33]
        io = [10, 11]
        if instr[1] in ls:
            ls_obj = LS(storage)
            if instr[1] == 20:
                ls_obj.load(instr)
            if instr[1] == 21:
                ls_obj.store(instr)
        elif instr[1] in arith:
            arith_obj = Arithmetic(storage)
            if instr[1] == 30:
                arith_obj.add(instr)
            if instr[1] == 31:
                arith_obj.sub(instr)
            if instr[1] == 32:
                arith_obj.div(instr)
            if instr[1] == 33:
                arith_obj.mult(instr)
        elif instr[1] in io:
            io_obj = IO(storage)
            if instr[1] == 10:
                io_obj.read(instr)
            if instr[1] == 11:
                io_obj.write(instr)
        elif instr[1] in control:
            control_obj = Control(storage)
            if instr[1] == 40:
                control_obj.branch(instr)
            if instr[1] == 41:
                control_obj.branch_neg(instr)
            if instr[1] == 42:
                control_obj.branch_zero(instr)
            if instr[1] == 43:
                control_obj.halt()
        else:
            continue
        storage.loc += 1


main()
