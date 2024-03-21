from memory import Memory
from cpu import CPU


class UVSimulator:
    def __init__(self):
        self.memory = Memory()
        self.cpu : CPU = CPU(self.memory)
        # IO_callbacks are functions that will be called if the program requests User input or to write to the UI
        self.IO_callbacks = {"read":None, "write":None}
        self.waiting_io = False

    def read_file(self, file):
        return self.memory.read_file(file)

    def load_program(self, memory_list = None):
        print(self.memory.loc)
        self.memory.set_loc(0)
        self.memory.memory = {}
        if memory_list is None:
            return 1
        self.memory.load_memory(memory_list= memory_list)
        return 0
    
    def get_memory(self):
        return self.memory.memory
    
    def resume_execution(self, input_instruction = None):
        self.waiting_io = False
        # if input_instruction is not None:
        #     int_instruction = [input_instruction[0], int(input_instruction[1:3]), int(input_instruction[3:5])]
        while self.memory.loc < len(self.memory.memory) and self.waiting_io == False:
            instruction = self.memory.memory[self.memory.loc]
            # print(f"location: {self.memory.loc}, instruction: {instruction}")
            # print(f"location #9: {self.memory.memory[9]}")
            self.execute_instruction(instruction, input_instruction=input_instruction)
            if self.waiting_io == False:
                self.memory.loc += 1
            input_instruction = None

    def execute_instruction(self, instruction, input_instruction = None):
        if self.memory.check_valid_instruction(instruction):
            result = self.cpu.execute(instruction, user_input = input_instruction)
            # print(self.memory.loc)
            if result == self.cpu.io.read:
                # print("calling read callback from uvsim")
                self.waiting_io = True
                self.IO_callbacks["read"]()
            elif result == self.cpu.io.write:
                self.waiting_io = True
                self.IO_callbacks["write"](self.get_memory())
                
    def run_program(self, read_callback, write_callback):
        self.IO_callbacks["read"] = read_callback
        self.IO_callbacks["write"] = write_callback
        # print(self.memory.loc)
        while self.memory.loc < len(self.memory.memory) and self.waiting_io == False:
            instruction = self.memory.memory[self.memory.loc]
            # print(f"location: {self.memory.loc}, instruction: {instruction}")
            # print(f"location #9: {self.memory.memory[9]}")
            self.execute_instruction(instruction)
            if self.waiting_io == False:
                self.memory.loc += 1

    def get_memory(self):
        # Retrieves from memory the value at the current memory location
        instruction = self.memory.memory[self.memory.loc]
        for i in range(len(instruction)):
            instruction[i] = str(instruction[i])
        return "".join(instruction)