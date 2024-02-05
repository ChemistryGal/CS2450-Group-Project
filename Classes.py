def check_valid_instruction(instruction):
    valid_ins = ["00","10","11","20","21","30","31","32","33","40","41","42","43"]
    if instruction in valid_ins:
        return True
    return False

class Storage:
    def __init__(self):
        self.memory = {} # Dictionary might be best to store each address and register.
        self.accumulator = 0
        self.loc = 0

    def set_loc(self,new_loc):
        self.loc = new_loc

    def load_memory(self, file):
        with open(file, "r") as f:
            loc = 0
            for line in f:
                self.memory[loc] = line
                loc += 1
        self.loc = 0

    def validate_memory(self):
        incorrect = []
        for instruction in self.memory.values():
            if check_valid_instruction(instruction[1:3]) == False:
                incorrect.append(instruction.strip())
        if len(incorrect) > 0:
            return incorrect
        else:
            return True

class Control:
    def __init__(self,storage):
        self.storage = storage

    def branch(self, instr):
        new_loc = int(instr[-2:])
        if new_loc not in self.storage.memory.keys():
            print(f'Invalid memory location. Please check your file.')
            self.storage.set_loc(101)
        else:
            self.storage.set_loc(new_loc)
        
    
    def branch_zero(self, instr):
        new_loc = int(instr[-2:])
        if new_loc not in self.storage.memory.keys():
            print(f'Invalid memory location. Please check your file.')
            self.storage.set_loc(101)
        elif self.storage.accumulator == 0:
            self.storage.set_loc(new_loc)

    def branch_neg(self, instr):
        new_loc = int(instr[-2:])
        if new_loc not in self.storage.memory.keys():
            print(f'Invalid memory location. Please check your file.')
            self.storage.set_loc(101)
        elif self.storage.accumulator < 0:
            self.storage.set_loc(new_loc)

    def halt(self, instr):
        self.storage.loc = 101

class IO:
    def __init__(self,storage):
        self.storage = storage

    def read(self, instr):
        print("read", instr)

    def write(self, instr):
        print("write", instr)

class LS:
    def __init__(self,storage):
        self.storage = storage

    def load(self, instr):
        print("load", instr)

    def store(self, instr):
        print("store", instr)

class Arithmetic:
    def __init__(self,storage):
        self.storage = storage

    def add(self, instr):
        print("add", instr)

    def sub(self, instr):
        print("sub", instr)

    def div(self, instr):
        print("div", instr)

    def mult(self, instr):
        print("mult", instr)
