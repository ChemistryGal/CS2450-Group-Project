def check_valid_instruction(instruction):
    valid_ins = ["00", "10", "11", "20", "21", "30",
                 "31", "32", "33", "40", "41", "42", "43"]
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
                self.memory[loc] = line.strip()
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

    # Returns the value at the specified location in memory (mem_key)
    def read_memory(self, mem_key):
        return self.memory[mem_key]

    # Writes the value to the specified location in memory (mem_key)
    def write_memory(self, mem_key, val):
        self.memory[mem_key] = val


class Control:
    def __init__(self, storage):
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

    def halt(self):
        self.storage.loc = 101


class IO:
    def __init__(self, storage):
        self.storage = storage

    def read(self, instr):
        while True:
            input_string = input("Enter a signed four-digit number: ")
            try:
                # Attempt to convert input to an integer
                mem_value = int(input_string)
                if -9999 <= mem_value <= 9999:
                    mem_key = int(instr[3:5])
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
        print(self.storage.read_memory(int(instr[3:5])))


class LS:
    def __init__(self, storage: Storage):
        self.storage = storage

    def load(self, location: str):
        int_location = int(location)
        self.storage.accumulator = int(self.storage.memory[int_location])
        # print(f"Loaded accumulator with value at memory location: {location} accumulator value: {self.storage.accumulator}")

    def store(self, location: str):
        int_location = int(location)
        if self.storage.accumulator == 0:
            self.storage.memory[int_location] = "+0000"
        else:
            self.storage.memory[int_location] = str(self.storage.accumulator)
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

    def add(self, location: str):
        int_location = int(location)
        other = int(self.storage.memory[int_location])
        self.storage.accumulator += other
        # print(f"Added accumulator value: {self.storage.accumulator}")

    def sub(self, location: str):
        int_location = int(location)
        other = int(self.storage.memory[int_location])
        self.storage.accumulator -= other
        # print(f"Subtracted accumulator value: {self.storage.accumulator}")

    def div(self, location: str):
        int_location = int(location)
        other = int(self.storage.memory[int_location])
        self.storage.accumulator /= other
        # print(f"Divided accumulator value: {self.storage.accumulator}")

    def mult(self, location: str):
        int_location = int(location)
        other = int(self.storage.memory[int_location])
        self.storage.accumulator *= other
        # print(f"Multiplied accumulator value: {self.storage.accumulator}")
