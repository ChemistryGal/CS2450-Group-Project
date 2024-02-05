from Classes import Storage, Control

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