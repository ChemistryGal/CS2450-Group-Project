from Classes import Storage, Control, Arithmetic, LS

#Control Operation Tests
def test_branch_1():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    ctrl = Control(storage)
    ctrl.branch("+4001")
    assert storage.loc == 1

def test_branch_2():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4099, 99:0000}
    ctrl = Control(storage)
    ctrl.branch("+4099")
    assert storage.loc == 99

def test_branch_3():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    ctrl = Control(storage)
    ctrl.branch("+4004")
    assert storage.loc == 101

def test_branch_neg_1():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    storage.accumulator = -1
    ctrl = Control(storage)
    ctrl.branch_neg("+4003")
    assert storage.loc == 3

def test_branch_neg_2():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    storage.accumulator = 0
    ctrl = Control(storage)
    ctrl.branch_neg("+4003")
    assert storage.loc == 0
    
def test_branch_neg_3():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    storage.accumulator = -1
    ctrl = Control(storage)
    ctrl.branch_neg("+4004")
    assert storage.loc == 101

def test_branch_zero_1():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    storage.accumulator = 0
    ctrl = Control(storage)
    ctrl.branch_zero("+4003")
    assert storage.loc == 3

def test_branch_zero_2():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    storage.accumulator = 1234
    ctrl = Control(storage)
    ctrl.branch_zero("+4003")
    assert storage.loc == 0
    
def test_branch_zero_3():
    storage = Storage()
    storage.memory = {0:1001, 1:1002, 2:4003, 3:0000}
    storage.accumulator = -1
    ctrl = Control(storage)
    ctrl.branch_zero("+4004")
    assert storage.loc == 101

def test_multiply_1():
    storage = Storage()
    storage.memory = {0:"1001", 1:"1002", 2:"4003", 3:"0003"}
    storage.accumulator = 10
    arithmetic = Arithmetic(storage)
    arithmetic.mult("03")
    assert storage.accumulator == 30

def test_multiply_2():
    storage = Storage()
    storage.memory = {0:"10", 1:"0002", 2:"4003", 3:"0003"}
    storage.accumulator = 4
    arithmetic = Arithmetic(storage)
    arithmetic.mult("01")
    assert storage.accumulator == 8

def test_multiply_3():
    storage = Storage()
    storage.memory = {0:"1001", 1:"0002", 2:"4003", 3:"0003"}
    storage.accumulator = 25
    arithmetic = Arithmetic(storage)
    arithmetic.mult("01")
    assert storage.accumulator == 50

def test_load_1():
    storage = Storage()
    storage.memory = {0:"1001", 1:"0002", 2:"4003", 3:"0003"}
    loader = LS(storage)
    to_load = ["00", "01", "02", "03"]
    for word in range(len(to_load)):
        print("iteration number: ", word)
        if word == 0:
            loader.load(to_load[word])
            assert storage.accumulator == 1001
        elif word == 1:
            loader.load(to_load[word])
            assert storage.accumulator == 2
        elif word == 2:
            loader.load(to_load[word])
            assert storage.accumulator == 4003
        elif word == 3:
            loader.load(to_load[word])
            assert storage.accumulator == 3

def test_load_1():
    storage = Storage()
    storage.memory = {0:"1001", 1:"0002", 2:"4003", 3:"0003"}
    loader = LS(storage)
    to_load = ["00", "01", "02", "03"]
    for word in range(len(to_load)):
        print("iteration number: ", word)
        if word == 0:
            loader.load(to_load[word])
            assert storage.accumulator == 1001
        elif word == 1:
            loader.load(to_load[word])
            assert storage.accumulator == 2
        elif word == 2:
            loader.load(to_load[word])
            assert storage.accumulator == 4003
        elif word == 3:
            loader.load(to_load[word])
            assert storage.accumulator == 3

def test_load_2():
    storage = Storage()
    storage.memory = {0:"01", 1:"0002", 2:"0003", 3:"04"}
    loader = LS(storage)
    to_load = ["00", "01", "02", "03"]
    for word in range(len(to_load)):
        if word == 0:
            loader.load(to_load[word])
            assert storage.accumulator == 1
        elif word == 1:
            loader.load(to_load[word])
            assert storage.accumulator == 2
        elif word == 2:
            loader.load(to_load[word])
            assert storage.accumulator == 3
        elif word == 3:
            loader.load(to_load[word])
            assert storage.accumulator == 4

def test_load_3():
    storage = Storage()
    storage.memory = {0:"0001", 1:"02", 2:"2103", 3:"4300"}
    loader = LS(storage)
    to_load = ["00", "01", "02", "03"]
    for word in range(len(to_load)):
        if word == 0:
            loader.load(to_load[word])
            assert storage.accumulator == 1
        elif word == 1:
            loader.load(to_load[word])
            assert storage.accumulator ==2
        elif word == 2:
            loader.load(to_load[word])
            assert storage.accumulator == 2103
        elif word == 3:
            loader.load(to_load[word])
            assert storage.accumulator == 4300