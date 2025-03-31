import math
import sys
from math import sin, radians

### Loosely based on "The Physics of Putting", Penner (2002)
# http://www.raypenner.com/golf-putting.pdf

COF = {
    6: 0.0,
    7: 0.,
    8: 0.0,
    9: 0.0,
    10: 0.0979,
    11: 0.0,
    12: 0.0655,
    13: 0.0
}


def roll(percent_grade, stimp, angle_of_hit, vel=72):
    """
    :param percent_grade: The side slope of the putt, as measured in percent grade (ex: float(3.5) == 3.5% grade)
    :param stimp: Green stimp as an integer (ex: 10)
    :param v:
    :return: A tuple of the distance rolled in inches, and the number of seconds it took to roll
    """
    mass_of_ball = 1
    g = 32 * 12  # Gravity in inches per second per second
    slope_in_radians = math.atan(percent_grade / 100.0)
    cp_distance_from_com = COF[stimp]
    ticks_per_second = 1000
    period = 1 / ticks_per_second
    phi = math.atan((cp_distance_from_com * math.cos(slope_in_radians) * math.sin(angle_of_hit)) / ((cp_distance_from_com * math.cos(slope_in_radians) * math.cos(slope_in_radians)) - ((2/5) * math.sin(slope_in_radians))))
    backwards_force = ((cp_distance_from_com * math.cos(slope_in_radians) * math.cos(angle_of_hit)) * mass_of_ball * g) / ((1 + (2/5)) * math.cos(phi))

    x_accel = (backwards_force * math.sin(phi)) / mass_of_ball
    y_accel = (g * math.sin(slope_in_radians)) - ((backwards_force * math.cos(phi)) / mass_of_ball)

    x_vel = vel * math.sin(angle_of_hit)
    y_vel = vel * math.cos(angle_of_hit)

    distance = 0
    seconds = 0

    count = 0
    while x_vel >= 0 and y_vel >= 0:
        x_vel += x_accel * period
        y_vel += y_accel * period

        x_displacement = (x_vel * period) - (0.5 * x_accel * period)
        y_displacement = (y_vel * period) - (0.5 * y_accel * period)

        distance += math.sqrt(x_displacement ** 2 + y_displacement ** 2)
        seconds += period
        count += 1

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

# Ball is moving 72 inches per second at the bottom of a stimpmeter ramp, so that's the default velocity
    v = 72
    if len(sys.argv) == 4:
        v = float(sys.argv[3])

    print(f"On a stimp {stimp} green with a {slope}% slope at {v} inches per second ({v/17.6} mph):")

    flat_distance, flat_seconds = roll(0, stimp, 0, v)

    up_distance, up_seconds = roll(slope, stimp, 0, v)

    print("Went up %f feet (%f) in %f seconds" % (up_distance, up_distance - stimp, up_seconds))
    #print("Up Scaling factor: %f" % (flat_distance / up_distance))

    down_distance, down_seconds = roll(-slope, stimp, 0, v)
    assert down_distance is not None, "Ball will never stop going down!"
    print("Went down %f feet (+%f) in %f seconds" % (down_distance, down_distance - stimp, down_seconds))
    #print("Down Scaling factor: %f" % (flat_distance / down_distance))
