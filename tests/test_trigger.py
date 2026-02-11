from aidbg.logic.complexity import classify_error

def test_simple_error_detection():
    tb = "ZeroDivisionError: division by zero"
    assert classify_error(tb) == "simple"
