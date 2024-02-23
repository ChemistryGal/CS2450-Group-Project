def check_valid_instruction(instruction):
    valid_ins = [10, 11, 20, 21, 30,
                 31, 32, 33, 40, 41, 42, 43]
    if instruction in valid_ins:
        return True
    return False

class Storage:
    def __init__(self):
        # Dictionary might be best to store each address and register.
        self.memory = {}
        self.accumulator = 0
        self.loc = 0

    def set_loc(self, new_loc):
        self.loc = new_loc

    def load_memory(self, file):
        with open(file, "r") as f:
            loc = 0
            for line in f:
                clean = line.strip()
                if check_valid_instruction(int(clean[1:3])):
                    self.memory[loc] = [clean[0:1], int(clean[1:3]), int(clean[3:5])]
                loc += 1
        self.loc = 0

    # Returns the value at the specified location in memory (mem_key)
    def read_memory(self, mem_key):
        return self.memory[mem_key]

    # Writes the value to the specified location in memory (mem_key)
    def write_memory(self, mem_key, val):
        self.memory[mem_key] = val

    def format(self, instr):
        if instr[0] == '+':
             return int(str(instr[1])+str(instr[2]))
        else:
            return int('-'+str(instr[1])+str(instr[2]))
    