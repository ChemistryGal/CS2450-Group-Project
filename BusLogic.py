from Storage import Storage
from Classes import *

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
