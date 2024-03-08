from Classes import *
from memory import Memory

class CPU:
    def __init__(self, memory : Memory) -> None:
        self.storage = memory
        self.io = IO(memory)
        self.control = Control(memory)
        self.load_store = LS(memory)
        self.arithmetic = Arithmetic(memory)

    def execute(self, instruction, **kwargs):
        opcode = instruction[1]
        commands = {
            10: self.io.read,
            11: self.io.write, 
            20: self.load_store.load, 
            21: self.load_store.store, 
            30: self.arithmetic.add, 
            31: self.arithmetic.sub, 
            32: self.arithmetic.div, 
            33: self.arithmetic.mult, 
            40: self.control.branch, 
            41: self.control.branch_neg, 
            42: self.control.branch_zero, 
            43: self.control.halt
            }
        if commands[opcode] == self.io.read and kwargs["user_input"] :
            return commands[opcode](instruction, kwargs["user_input"])
        return commands[opcode](instruction)
        