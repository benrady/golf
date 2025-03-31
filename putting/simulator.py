import math
import sys
from math import sin, radians

### From "The Physics of Putting", Penner (2002)
# http://www.raypenner.com/golf-putting.pdf

INITIAL_STIMPMETER_VELOCITY = 72 # inches per second

def roll(percent_grade, stimp, v=INITIAL_STIMPMETER_VELOCITY):
    """
    :param percent_grade: The side slope of the putt, as measured in percent grade (ex: float(3.5) == 3.5% grade)
    :param stimp: Green stimp as an integer (ex: 10)
    :param v: initial velocity in inches per second
    :return: A tuple of the distance rolled in inches, and the number of seconds it took to roll
    """
    slope_radians = math.atan(percent_grade / 100.0)

    # Weber and Magnum both model the CoF as a C/X function, so I've used a power regression
    # to fit the data using the 4 and 12 stimp values from Penner.
    # https://www.desmos.com/calculator/5pu5wa05ef
    friction = 0.789077/stimp

    ticks_per_second = 1000
    g = 32 * 12 # Gravity in inches per second per second
    period = 1 / ticks_per_second

    # Velocity adjustment due to friction of the rolling ball
    drag = -(5/7) * friction * g * period

    # Velocity adjustment due to gravity, deflected by the slope
    drop = -g * sin(slope_radians) * period

    if drag + drop >= 0:
        # If the loop would run infinitely, return now
        return None, None

    distance = 0
    seconds = 0
    while v > 0:
        v = v + drop + drag

        distance += v * period
        seconds += period

    return (distance / 12), seconds


def inches_of_break(percent_grade, stimp, distance):
    """
    :param percent_grade: The side slope of the putt, as measured in percent grade (ex: float(3.5) == 3.5% grade)
    :param stimp: Green stimp as an integer (ex: 10)
    :param distance: Distance in feet
    :return: Break in inches
    """
    # Formula from Geoff Mangum https://swingmangolf.com/putting-zone-basic-math/
    return distance * percent_grade * stimp / 20


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: python3 ./stimpmeter.py <slope in % grade> <speed in stimp> [initial speed in in/sec]")
        sys.exit(0)
    slope = float(sys.argv[1]) # Slope in percent grade
    stimp = int(sys.argv[2]) # Speed of the green as measured by a stimpmeter

    v = INITIAL_STIMPMETER_VELOCITY
    if len(sys.argv) == 4:
        v = float(sys.argv[3])

    print(f"On a stimp {stimp} green with a {slope}% slope at {v} inches per second ({v/17.6} mph):")

    flat_distance, flat_seconds = roll(0, stimp, v)

    up_distance, up_seconds = roll(slope, stimp, v)

    print("Went up %f feet (%f) in %f seconds" % (up_distance, up_distance - stimp, up_seconds))
    print("Up Scaling factor: %f" % (flat_distance / up_distance))

    down_distance, down_seconds = roll(-slope, stimp, v)
    assert down_distance is not None, "Ball will never stop going down!"
    print("Went down %f feet (+%f) in %f seconds" % (down_distance, down_distance - stimp, down_seconds))
    print("Down Scaling factor: %f" % (flat_distance / down_distance))
