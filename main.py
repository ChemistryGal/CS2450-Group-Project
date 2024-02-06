from Classes import *

def main():
    # Get user input
    file = input("Hello! Welcome to UVUSim. Please type the name of your txt file: ")
    #Create storage obj and load data into memory
    storage = Storage()
    storage.load_memory(file)
    # Validate the memory that was loaded. Throw an error if there is an incorrect instruction throw a error meesage to the console.
    if type(storage.validate_memory()) == list:
        bad = storage.validate_memory()
        print(f'There seems to be an issue with the following instruction/s in your file: {bad}')
    else:
        while storage.loc <= len(storage.memory):
            instr = storage.memory[storage.loc]
            control = ["40","41","42","43"]
            ls = ["20","21"]
            arith = ["30", "31", "32","33"]
            io = ["10","11"]
            if instr[1:3] in ls:
                ls_obj = LS(storage)
                if instr[1:3] == "20":
                    ls_obj.load(instr[3:5])
                if instr[1:3] == "21":
                    ls_obj.store(instr[3:5])
            if instr[1:3] in arith:
                arith_obj = Arithmetic(storage)
                if instr[1:3] == "30":
                    arith_obj.add(instr)
                if instr[1:3] == "31":
                    arith_obj.sub(instr)
                if instr[1:3] == "32":
                    arith_obj.div(instr)
                if instr[1:3] == "33":
                    arith_obj.mult(instr[3:5])
            if instr[1:3] in io:
                io_obj = IO(storage)
                if instr[1:3] == "10":
                    io_obj.read(instr)
                if instr[1:3] == "11":
                    io_obj.write(instr)
            if instr[1:3] in control:
                control_obj = Control(storage)
                if instr[1:3] == "40":
                    control_obj.branch(instr)
                if instr[1:3] == "41":
                    control_obj.branch_neg(instr)
                if instr[1:3] == "42":
                    control_obj.branch_zero(instr)
                if instr[1:3] == "43":
                    control_obj.halt(instr)
            storage.loc += 1
    
main()
