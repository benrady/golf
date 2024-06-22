import sys
import io
import csv

from putting import stimpmeter

def ratio(slope: int, stimp: int) -> float:
    """
    :param slope: Percent grade slope as a signed integer value. int(3) is 3% up, int(-6) is 6% down
    :param stimp: Green stimp
    :return: The speed ratio vs a flat putt on a stimp 10 green
    """
    if slope == 0:
        return round(100 * 10.0 / stimp)
     # Should be the same as the stimp, but we're correcting for error
    flat_distance, _ = stimpmeter.calculate(0, stimp)

    distance, _ = stimpmeter.calculate(slope, stimp)
    if distance is None:
        return 0
    return round((10 * 100 * flat_distance) / (distance * stimp))

def generate_csv(out: io.TextIOBase) -> None:
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(range(8, 14))
    for slope in range(7, -8, -1):
        writer.writerow([slope] + [ratio(slope, stimp) for stimp in range(8, 14)])

if __name__ == "__main__":
    generate_csv(sys.stdout)
