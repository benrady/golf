from putting import simulator


def test_break():
    assert simulator.inches_of_break(1, 10, 10) == 5.0
    assert simulator.inches_of_break(2, 10, 10) == 10.0
    assert simulator.inches_of_break(2, 10, 20) == 20.0
    assert simulator.inches_of_break(0, 10, 10) == 0.0
    assert simulator.inches_of_break(5, 10, 0) == 0.0