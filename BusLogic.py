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
        elif instr[0] == '-':
            return int('-'+str(instr[1])+str(instr[2]))
        else:
            return int(instr)
    
class ArithLogic:
        
    def check_overflow(self, result):
        if len(str(result)) > 4 and result>0:
            temp = str(result)[:4]
            self.storage.accumulator = int(temp)
        elif len(str(result)) > 4 and result<0:
            temp = str(result)[:5]
            self.storage.accumulator = int(temp)
        else:
            self.storage.accumulator = result

class UVSimulator:
    def __init__(self):
        self.storage = Storage()
        self.commands = {
            20: LS(self.storage).load,
            21: LS(self.storage).store,
            30: Arithmetic(self.storage).add,
            31: Arithmetic(self.storage).sub,
            32: Arithmetic(self.storage).div,
            33: Arithmetic(self.storage).mult,
            10: IO(self.storage).read,
            11: IO(self.storage).write,
            40: Control(self.storage).branch,
            41: Control(self.storage).branch_neg,
            42: Control(self.storage).branch_zero,
            43: Control(self.storage).halt
        }
        # This is what connects the User interface to the commands.
        self.shared_input = None
        self.shared_output = None
        
    def load_program(self, file):
        if file is None:
            return 1
        self.storage.load_memory(file)
        return 0

    def execute_instruction(self, instr):
        opcode = instr[1]
        if opcode in self.commands:
            self.commands[opcode](instr)

    def run_program(self):
        while self.storage.loc < len(self.storage.memory):
            instr = self.storage.memory[self.storage.loc]
            self.execute_instruction(instr)
            self.storage.loc += 1

