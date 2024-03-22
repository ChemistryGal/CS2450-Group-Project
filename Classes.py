from UVsimulator import *
from memory import Memory

# class ArithLogic:
#     def check_overflow(self, result):
#         if len(str(result)) > 4 and result>0:
#             temp = str(result)[:4]
#             self.storage.accumulator = int(temp)
#         elif len(str(result)) > 4 and result<0:
#             temp = str(result)[:5]
#             self.storage.accumulator = int(temp)
#         else:
#             self.storage.accumulator = result

#     def check_valid_instruction(instruction):
#         valid_ins = [10, 11, 20, 21, 30,
#                     31, 32, 33, 40, 41, 42, 43]
#         if instruction in valid_ins:
#             return True
#         return False

class Control:
    def __init__(self, storage :Memory):
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

    def halt(self, instr):
        print(f"HAULT at memory location: {self.storage.loc}")
        self.storage.loc = 101


class IO:
    def __init__(self, storage: Memory):
        self.storage = storage

    def read(self, instruction, user_input = None):
            if user_input is None:
                return self.read
            input_string = user_input
            if self.storage.check_valid_instruction(self.storage.read_memory(instruction[2])):
                print("Oh no! You overwriting a memory location that has a valid instruction in it currently. Please review you txt file.")
                self.storage.set_loc(101)
            try:
                # Attempt to convert input to an integer
                if len(input_string) == 5:
                    mem_value = [input_string[0], int(input_string[1:3]), int(input_string[3:5])]
                    mem_key = instruction[2]
                    # Input is valid; exit the loop
                    self.storage.write_memory(mem_key, mem_value)
                    # print(self.storage.memory[mem_key])
                else:
                    raise ValueError  # Input is not within the valid range
            except ValueError:
                # This block executes if the input is not a valid integer or not in the range
                print("Invalid input. Please enter a signed four-digit number.")
                return self.read
            

    def write(self, instruction):
        # prints the returned value of the read_memory method
        item = self.storage.read_memory(instruction[2])
        if type(item) == list:
            res_str = self.storage.format(item)
        else:
            res_str = item
        # print(res_str)
        return self.write

class LS:
    def __init__(self, storage: Memory):
        self.storage = storage

    def load(self, instruction:list):
        int_location = instruction[2]
        if int_location in self.storage.memory.keys():
            self.storage.accumulator = self.storage.format(self.storage.memory[int_location])
        else:
            self.storage.set_loc(101)
            print(f'Memory location {int_location} is empty! Please review you txt file to make sure you are referencing the coprrect location.')
        # print(f"Loaded accumulator with value at memory location: {location} accumulator value: {self.storage.accumulator}")

    def store(self, instruction:list):
        int_location = instruction[2]
        if self.storage.accumulator == 0:
            self.storage.memory[int_location] = ["+", 0, 0]
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

    def __init__(self, storage: Memory):
        self.storage = storage

    def add(self, instruction: list):
        int_location = instruction[2]
        other = self.storage.format(self.storage.memory[int_location])
        accu = self.storage.accumulator
        result = accu + other
        self.check_overflow(result)
        # print(f"Added accumulator value: {self.storage.accumulator}")

    def sub(self, instruction: list):
        int_location = instruction[2]
        accu = self.storage.accumulator
        other = self.storage.format(self.storage.memory[int_location])
        result = accu - other
        self.check_overflow(result)
        # print(f"Subtracted accumulator value: {self.storage.accumulator}")

    def div(self, instruction: list):
        int_location = instruction[2]
        accu = self.storage.accumulator
        other = self.storage.format(self.storage.memory[int_location])
        result = accu/other
        self.check_overflow(result)
        # print(f"Divided accumulator value: {self.storage.accumulator}")

    def mult(self, instruction: list):
        int_location = instruction[2]
        accu = self.storage.accumulator
        other = self.storage.format(self.storage.memory[int_location])
        result = accu*other
        self.check_overflow(result)
        # print(f"Multiplied accumulator value: {self.storage.accumulator}")

    def check_overflow(self, result):
        if len(str(result)) > 4 and result>0:
            temp = str(result)[:4]
            self.storage.accumulator = int(temp)
        elif len(str(result)) > 4 and result<0:
            temp = str(result)[:5]
            self.storage.accumulator = int(temp)
        else:
            self.storage.accumulator = result
