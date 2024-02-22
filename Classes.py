def check_valid_instruction(instruction):
    valid_ins = [10, 11, 20, 21, 30,
                 31, 32, 33, 40, 41, 42, 43] # change to numbers
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
                else:
                    self.memory[loc] = clean
                loc += 1
        self.loc = 0

    # Returns the value at the specified location in memory (mem_key)
    def read_memory(self, mem_key):
        return self.memory[mem_key]

    # Writes the value to the specified location in memory (mem_key)
    def write_memory(self, mem_key, val):
        self.memory[mem_key] = val


    # # Returns the value at the specified location in memory (mem_key)
    # def read_memory(self, mem_key):
    #     return self.memory[mem_key]

    # # Writes the value to the specified location in memory (mem_key)
    # def write_memory(self, mem_key, val):
    #     self.memory[mem_key] = val


class Control:
    def __init__(self, storage :Storage):
        self.storage = storage

    # This function will branch to a new memory location
    def branch(self, instr: list):
        new_loc = int(instr[2])
        if new_loc not in self.storage.memory.keys():
            print(f'Invalid memory location. Please check your file.')
            self.storage.set_loc(101)
        else:
            self.storage.set_loc(new_loc-1)

    # This function will branch to anew memory location if the accumulator is zero
    def branch_zero(self, instr: list):
        new_loc = int(instr[2])
        if new_loc not in self.storage.memory.keys():
            print(f'Invalid memory location. Please check your file.')
            self.storage.set_loc(101)
        elif self.storage.accumulator == 0:
            self.storage.set_loc(new_loc-1)

    # This function will branch to anew memory location if the accumulator is negative
    def branch_neg(self, instr:list):
        new_loc = int(instr[2])
        if new_loc not in self.storage.memory.keys():
            print(f'Invalid memory location. Please check your file.')
            self.storage.set_loc(101)
        elif self.storage.accumulator < 0:
            self.storage.set_loc(new_loc-1)

    def halt(self):
        self.storage.loc = 101


class IO:
    def __init__(self, storage: Storage):
        self.storage = storage

    def read(self, instr):
        while True:
            input_string = input("Enter a signed four-digit number: ")
            if check_valid_instruction(self.storage.memory[instr[2]][1]):
                print("Oh no! You overwriting a memory location that has a valid instruction in it currently. Please review you txt file.")
                self.storage.set_loc(101)
            try:
                # Attempt to convert input to an integer
                mem_value = input_string
                if len(mem_value) == 4:
                    mem_key = instr[2]
                    # Input is valid; exit the loop
                    self.storage.write_memory(mem_key, mem_value)
                    break
                else:
                    raise ValueError  # Input is not within the valid range
            except ValueError:
                # This block executes if the input is not a valid integer or not in the range
                print("Invalid input. Please enter a signed four-digit number.")

                # print("read", instr)

    def write(self, instr):
        # prints the returned value of the read_memory method
        item = self.storage.read_memory(instr[2])
        if type(item) == list:
            res_str = ''.join(str(item) for item in item)
        else:
            res_str = item
        print(res_str)


class LS:
    def __init__(self, storage: Storage):
        self.storage = storage

    def load(self, instr:list):
        int_location = instr[2]
        if int_location in self.storage.memory.keys():
            if type(self.storage.memory[int_location]) == list:
                if instr[0] == '+':
                    self.storage.accumulator = int(str(self.storage.memory[int_location][1])+str(self.storage.memory[int_location][2]))
                else:
                    self.storage.accumulator = int('-'+str(self.storage.memory[int_location][1])+str(self.storage.memory[int_location][2]))
            else:
                self.storage.accumulator =int(self.storage.memory[int_location])
        else:
            self.storage.set_loc(101)
            print(f'Memory location {instr[2]} is empty! Please review you txt file to make sure you are referencing the coprrect location.')
        # print(f"Loaded accumulator with value at memory location: {location} accumulator value: {self.storage.accumulator}")

    def store(self, instr:list):
        int_location = instr[2]
        if self.storage.accumulator == 0:
            self.storage.memory[int_location] = "+0000"
        else:
            self.storage.memory[int_location] = self.storage.accumulator
        # print(f"Stored {self.storage.accumulator} at location {location}")


class Arithmetic:
    """integer arithmetic

    We want to keep the strings subscriptable so that the command line interface will work.
    This makes arithmetic more complicated. The load function casts values into integers.
    The accumulator can only store integers. Cast strings into integers in order to implement
    these functions.

    - Nick
    """

    def __init__(self, storage: Storage):
        self.storage = storage

    def check_overflow(self, result):
        if len(str(result)) > 4 and result>0:
            temp = str(result)[:4]
            self.storage.accumulator = int(temp)
        elif len(str(result)) > 4 and result<0:
            temp = str(result)[:5]
            self.storage.accumulator = int(temp)
        else:
            self.storage.accumulator = result

    def add(self, instr: list):
        other = instr[2]
        # other = int(self.storage.memory[int_location])
        accu = self.storage.accumulator
        result = accu + other
        self.check_overflow(result)
        # print(f"Added accumulator value: {self.storage.accumulator}")

    def sub(self, instr: list):
        other = instr[2]
        accu = self.storage.accumulator
        # other = int(self.storage.memory[int_location])
        result = accu - other
        self.check_overflow(result)
        # print(f"Subtracted accumulator value: {self.storage.accumulator}")

    def div(self, instr: list):
        other = instr[2]
        accu = self.storage.accumulator
        #  = int(self.storage.memory[int_location])
        result = accu/other
        self.check_overflow(result)
        # print(f"Divided accumulator value: {self.storage.accumulator}")

    def mult(self, instr: list):
        other = instr[2]
        accu = self.storage.accumulator
        # other = int(self.storage.memory[int_location])
        result = accu*other
        print(result)
        self.check_overflow(result)
        # print(f"Multiplied accumulator value: {self.storage.accumulator}")
