import io

from . import putting_factors


def test_calculate_putting_ratio():
    # The benchmark speed (100%) is on a flat, stimp 10 green
    assert putting_factors.ratio(0, 10) == 100

    # An uphill putt on a 3% grade, stimp 10 green will have to be hit at 142% speed
    # to go the same distance as a flat putt on a stimp 10 green
    assert putting_factors.ratio(3, 10) == 142

    # A downhill putt on a 7% grade, stimp 8 green, will have to be hit at 27% speed
    # to go the same distance as a flat putt on a stimp 10 green
    assert putting_factors.ratio(-7, 8) == 27

    # An uphill putt on a 7% grade, stimp 13 green, will have to be hit at 175% speed
    assert putting_factors.ratio(7, 13) == 175


def test_putts_that_dont_stop():
    assert putting_factors.ratio(-7, 11) == 0
    assert putting_factors.ratio(-6, 12) == 0


def test_csv_generation():
    string_io = io.StringIO()
    putting_factors.generate_csv(string_io)
    assert string_io.getvalue().strip() == """8,9,10,11,12,13
7,223,209,198,189,181,175
6,209,195,184,175,167,161
5,195,181,170,161,153,147
4,181,167,156,147,139,133
3,167,153,142,133,125,119
2,153,139,128,119,111,105
1,139,125,114,105,97,91
0,125,111,100,91,83,77
-1,111,97,86,77,69,63
-2,97,83,72,63,55,49
-3,83,69,58,49,41,35
-4,69,55,44,35,27,21
-5,55,41,30,21,13,7
-6,41,27,16,7,0,0
-7,27,13,2,0,0,0"""
