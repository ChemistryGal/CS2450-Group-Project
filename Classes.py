from BusLogic import *

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
            self.storage.accumulator = self.storage.format(instr)
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


class Arithmetic(ArithLogic):
    """integer arithmetic

    We want to keep the strings subscriptable so that the command line interface will work.
    This makes arithmetic more complicated. The load function casts values into integers.
    The accumulator can only store integers. Cast strings into integers in order to implement
    these functions.

    - Nick
    """

    def __init__(self, storage: Storage):
        self.storage = storage

    def add(self, instr: list):
        int_location = instr[2]
        other = self.storage.format(self.storage.memory[int_location])
        accu = self.storage.accumulator
        result = accu + other
        self.check_overflow(result)
        # print(f"Added accumulator value: {self.storage.accumulator}")

    def sub(self, instr: list):
        int_location = instr[2]
        accu = self.storage.accumulator
        other = self.storage.format(self.storage.memory[int_location])
        result = accu - other
        self.check_overflow(result)
        # print(f"Subtracted accumulator value: {self.storage.accumulator}")

    def div(self, instr: list):
        int_location = instr[2]
        accu = self.storage.accumulator
        other = self.storage.format(self.storage.memory[int_location])
        result = accu/other
        self.check_overflow(result)
        # print(f"Divided accumulator value: {self.storage.accumulator}")

    def mult(self, instr: list):
        int_location = instr[2]
        accu = self.storage.accumulator
        other = self.storage.format(self.storage.memory[int_location])
        result = accu*other
        print(result)
        self.check_overflow(result)
        # print(f"Multiplied accumulator value: {self.storage.accumulator}")
