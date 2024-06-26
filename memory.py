

class Memory:
    def __init__(self):
        # Dictionary might be best to store each address and register.
        self.memory = {}
        self.accumulator = 0
        self.loc = 0

    def set_loc(self, new_loc):
        self.loc = new_loc

    def four_to_six_formatting(self,value):
        break_up = [value[0:1], int(value[1:3]), int(value[3:5])]
        if self.check_valid_instruction(break_up):
            new_value = f'{value[0:1]}0{str(value[1:3])}0{str(value[3:5])}'
            return new_value
        else:
            new_value = f'{value[0:1]}00{str(value[1:])}'
            return new_value
        

    def read_file(self, file) -> list:
        if file == None:
            return 1
        with open(file, "r") as f:
            temp_memory = []
            for line in f:
                print(line)
                clean = line.strip()
                if len(clean)<7:
                    clean = self.four_to_six_formatting(clean)
                temp_memory.append(clean)
        f.close()
        return temp_memory

    def process6files(self, memory_list: list):
        i = 0
        while i < len(memory_list) and i <= 250:
                clean = memory_list[i].strip()
                self.memory[i] = [clean[0:1], int(clean[1:4]), int(clean[5:])]
                i += 1
        return clean

    def load_memory(self, memory_list:list):
        if len(memory_list[0]) == 7:
             self.process6files(memory_list)

        # i = 0
        # while i < len(memory_list) and i < 100:
        #         clean = memory_list[i].strip()
        #         self.memory[i] = [clean[0:1], int(clean[1:3]), int(clean[3:5])]
        #         i += 1
        # return clean
        
    # Returns the value at the specified location in memory (mem_key)
    def read_memory(self, mem_key):
        print(mem_key)
        print(self.memory)
        return self.memory[mem_key]

    # Writes the value to the specified location in memory (mem_key)
    def write_memory(self, mem_key, val):
        self.memory[mem_key] = val

    def format(self, instr):
        print(instr)
        if instr[0] == '+':
             return int(str(instr[1])+str(instr[2]))
        elif instr[0] == '-':
            return int('-'+str(instr[1])+str(instr[2]))
        else:
            return int(instr)

    def check_valid_instruction(self, instruction):
        opcode = instruction[1]
        valid_ins = [10, 11, 20, 21, 30,
                    31, 32, 33, 40, 41, 42, 43]
        if opcode in valid_ins:
            return True
        return False
