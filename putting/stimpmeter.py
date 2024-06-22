import sys
from math import sin, radians

COF = {
        6:  0.131,
        7:  0.1125,
        8:  0.0985,
        9:  0.0875,
        10: 0.0785,
        11: 0.0715,
        12: 0.0655,
        13: 0.0605}

def calculate(percent_grade, stimp, v=72):
    degrees = percent_grade / 2.22
    friction = COF[stimp]
    ticks_per_second = 1000
    g = 32 * 12 # Gravity in inches per second per second
    period = 1 / ticks_per_second

    ### From "The Physics of Putting", Penner (2002)
    # Force of friction
    drag = -(5/7) * friction * g * period

    ###

    # Force of gravity, deflected by the slope
    drop = -g * sin(radians(degrees)) * period

    if drag + drop >= 0:
        return None, None

    distance = 0
    seconds = 0
    while v > 0:
        v = v + drop + drag

        distance += v * period
        seconds += period

    return (distance / 12), seconds

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

    flat_distance, flat_seconds = calculate(0, stimp, v)

    up_distance, up_seconds = calculate(slope, stimp, v)

    print("Went up %f feet (%f) in %f seconds" % (up_distance, up_distance - stimp, up_seconds))
    print("Up Scaling factor: %f" % (flat_distance / up_distance))

    down_distance, down_seconds = calculate(-slope, stimp, v)
    assert down_distance is not None, "Ball will never stop going down!"
    print("Went down %f feet (+%f) in %f seconds" % (down_distance, down_distance - stimp, down_seconds))
    print("Down Scaling factor: %f" % (flat_distance / down_distance))
