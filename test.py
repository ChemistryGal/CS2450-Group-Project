import pytest
# run pip install pytest in your terminal before running
# pytest test.py


from Classes import *
from UVsimulator import *
from memory import Memory


@pytest.fixture
def storage():
    return Memory()


# Control Operation Tests


def test_branch_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1], 1: ["+", 10, 2],
                      2: ["+", 40, 3], 3: ["+", 0, 0]}
    ctrl = Control(storage)
    ctrl.branch(['+', 40, 1])
    assert storage.loc == 0


def test_branch_2():
    storage = Memory()
    # storage.memory = {0: 1001, 1: 1002, 2: 4099, 99: 0000}
    storage.memory = {0: ["+", 10, 1], 1: ["+", 10, 2],
                      2: ["+", 40, 99], 99: ["+", 0, 0]}
    ctrl = Control(storage)
    ctrl.branch(['+', 40, 99])
    assert storage.loc == 98


def test_branch_3():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 0]}
    ctrl = Control(storage)
    ctrl.branch(['+', 40, 4])
    assert storage.loc == 101


def test_branch_neg_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 0]}
    storage.accumulator = -1
    ctrl = Control(storage)
    ctrl.branch_neg(['+', 41, 3])
    assert storage.loc == 2


def test_branch_neg_2():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 0]}
    storage.accumulator = 0
    ctrl = Control(storage)
    ctrl.branch_neg(['+', 41, 1])
    assert storage.loc == 0


def test_branch_neg_3():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 0]}
    storage.accumulator = -1
    ctrl = Control(storage)
    ctrl.branch_neg(['+', 41, 4])
    assert storage.loc == 101


def test_branch_zero_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 0]}
    storage.accumulator = 0
    ctrl = Control(storage)
    ctrl.branch_zero(['+', 42, 3])
    assert storage.loc == 2


def test_branch_zero_2():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 0]}
    storage.accumulator = 1234
    ctrl = Control(storage)
    ctrl.branch_zero(['+', 40, 3])
    assert storage.loc == 0


def test_branch_zero_3():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 0]}
    storage.accumulator = -1
    ctrl = Control(storage)
    ctrl.branch_zero(['+', 40, 4])
    assert storage.loc == 101


def test_add_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 3]}
    storage.accumulator = 13
    arithmetic = Arithmetic(storage)
    arithmetic.add(['+', 0, 3])
    assert storage.accumulator == 16


def test_add_2():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 17]}
    storage.accumulator = 13
    arithmetic = Arithmetic(storage)
    arithmetic.add(['+', 0, 3])
    assert storage.accumulator == 30


def test_sub_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 3]}
    storage.accumulator = 23
    arithmetic = Arithmetic(storage)
    arithmetic.sub(['+', 0, 3])
    assert storage.accumulator == 20


def test_sub_2():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 3]}
    storage.accumulator = 9
    arithmetic = Arithmetic(storage)
    arithmetic.sub(['+', 0, 3])
    assert storage.accumulator == 6


def test_divide_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 2]}
    storage.accumulator = 30
    arithmetic = Arithmetic(storage)
    arithmetic.div(['+', 0, 3])
    assert storage.accumulator == 15


def test_divide_2():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 1]}
    storage.accumulator = 12
    arithmetic = Arithmetic(storage)
    arithmetic.div(['+', 0, 3])
    assert storage.accumulator == 12


def test_multiply_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 3]}
    storage.accumulator = 10
    arithmetic = Arithmetic(storage)
    arithmetic.mult(['+', 0, 3])
    assert storage.accumulator == 30


def test_multiply_2():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 4]}
    storage.accumulator = 4
    arithmetic = Arithmetic(storage)
    arithmetic.mult(['+', 0, 3])
    assert storage.accumulator == 16


def test_multiply_3():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 2]}
    storage.accumulator = 25
    arithmetic = Arithmetic(storage)
    arithmetic.mult(['+', 0, 3])
    assert storage.accumulator == 50

# def test_load_1():
#     storage = Storage()
#     storage.memory = {0: "1001", 1: "0002", 2: "4003", 3: "0003"}
#     loader = LS(storage)
#     to_load = ["00", "01", "02", "03"]
#     for word in range(len(to_load)):
#         print("iteration number: ", word)
#         if word == 0:
#             loader.load(to_load[word])
#             assert storage.accumulator == 1001
#         elif word == 1:
#             loader.load(to_load[word])
#             assert storage.accumulator == 2
#         elif word == 2:
#             loader.load(to_load[word])
#             assert storage.accumulator == 4003
#         elif word == 3:
#             loader.load(to_load[word])
#             assert storage.accumulator == 3


def test_load_1():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 4]}
    loader = LS(storage)
    loader.load(['+', 0, 3])
    assert storage.accumulator == 4


def test_load_2():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 4]}
    loader = LS(storage)
    loader.load(['+', 0, 2])
    assert storage.accumulator == 403


def test_load_3():
    storage = Memory()
    storage.memory = {0: ["+", 10, 1],
                      1: ["+", 10, 2], 2: ["+", 40, 3], 3: ["+", 0, 4]}
    loader = LS(storage)
    loader.load(['+', 0, 1])
    assert storage.accumulator == 102


def test_read_1(monkeypatch):
    # Simulate user input
    monkeypatch.setattr('builtins.input', lambda _: '1234')
    storage = Memory()
    storage.memory = {0: ['+', 10, 1], 1: ['+', 0, 0]}
    io = IO(storage)
    instr = ['+', 10, 1]
    io.read(instr)
    # Assert that the input value is stored in the correct memory location
    # Adjust this according to how you handle values in memory
    assert storage.memory[instr[2]] == '1234'


def test_read_2(monkeypatch):
    # Simulate user input
    input = '4321'
    monkeypatch.setattr('builtins.input', lambda _: input)
    storage = Memory()
    storage.memory = {0: ['+', 10, 1], 1: ['+', 0, 0]}
    io = IO(storage)
    instr = ['+', 10, 1]
    io.read(instr)
    # Assert that the input value is stored in the correct memory location
    # Adjust this according to how you handle values in memory
    assert storage.memory[instr[2]] == '4321'


def test_write_1(capfd):
    storage = Memory()
    io = IO(storage)
    mem_key = '01'
    instr = ['+',10,1]
    storage.memory[instr[2]] = 1234  # Pre-set a value in memory
    io.write(instr)
    out, _ = capfd.readouterr()
    # Assert that the output contains the expected value
    assert "1234" in out


def test_write_2(capfd):
    storage = Memory()
    io = IO(storage)
    mem_key = '01'
    instr = ['+', 10, 1]
    storage.memory[instr[2]] = -3456  # Pre-set a value in memory
    io.write(instr)
    out, _ = capfd.readouterr()
    # Assert that the output contains the expected value
    assert "-3456" in out


def test_halt():
    storage = Memory()
    control = Control(storage)
    control.halt(['+',10,1])  # Execute the halt command
    # Assert that the storage's instruction pointer indicates the program should halt
    # 101 is outside of the range of what storage locations is supposed to be
    assert storage.loc == 101
