import io

from . import putting_factors


def test_calculate_putting_ratio():
    # The benchmark speed (100%) is on a flat, stimp 10 green
    assert putting_factors.ratio(0, 10) == 100

    # An uphill putt on a 3% grade, stimp 10 green will have to be hit at 153% speed
    # to go the same distance as a flat putt on a stimp 10 green
    assert putting_factors.ratio(3, 10) == 153

    # A downhill putt on a 7% grade, stimp 8 green, will have to be hit at 1% speed
    # to go the same distance as a flat putt on a stimp 10 green
    assert putting_factors.ratio(-7, 8) == 1

    # An uphill putt on a 7% grade, stimp 13 green, will have to be hit at 201% speed
    assert putting_factors.ratio(7, 13) == 201


def test_putts_that_dont_stop():
    assert putting_factors.ratio(-7, 11) == 0
    assert putting_factors.ratio(-6, 12) == 0


def test_csv_generation():
    string_io = io.StringIO()
    putting_factors.generate_csv(string_io)
    assert string_io.getvalue().strip() == """8,9,10,11,12,13
7,249,235,224,215,207,201
6,231,217,206,197,190,183
5,214,200,189,180,172,166
4,196,182,171,162,154,148
3,178,164,153,144,137,130
2,160,147,135,126,119,112
1,143,129,118,109,101,95
0,125,111,100,91,83,77
-1,107,93,82,73,66,59
-2,90,76,65,55,48,41
-3,72,58,47,38,30,24
-4,54,40,29,20,12,6
-5,36,23,11,2,0,0
-6,19,5,0,0,0,0
-7,1,0,0,0,0,0"""
