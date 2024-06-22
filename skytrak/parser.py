import sys
import io
from typing import Iterable


def parse(in_stream: io.TextIOBase) -> Iterable[dict]:
    blank = next(in_stream)
    date_line = next(in_stream)
    player_line = next(in_stream)
    blank = next(in_stream)
    header_line = next(in_stream)
    club_line = next(in_stream)
    clubs = {}
    for line in in_stream:
        row = line.split(',')
    return clubs

def calculate_dispersion(club_data: Iterable[dict]):
    pass


if __name__ == "__main__":
    calculate_dispersion(parse(sys.stdin))
