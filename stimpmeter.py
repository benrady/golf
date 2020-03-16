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

def calculate(angle, stimp):
    friction = COF[stimp]
    ticks_per_second = 1000
    g = 32 * 12 # Gravity in inches per second per second
    period = 1 / ticks_per_second

    ### From "The Physics of Putting", Penner (2002)
    # Force of friction
    drag = -(5/7) * friction * g * period

    # Ball is moving 72 inches per second at the bottom of a stimpmeter ramp
    v = 72
    ###

    # Force of gravity, deflected by the slope
    drop = -g * sin(radians(angle)) * period

    assert drag + drop < 0, "Ball will never stop!"

    distance = 0
    seconds = 0
    while v > 0:
        v = v + drop + drag

        distance += v * period
        seconds += period

    return (distance / 12), seconds

slope = float(sys.argv[1]) # Slope in percent grade
stimp = int(sys.argv[2]) # Speed of the green as measured by a stimpmeter
degrees = slope / 2.22
print(f"On a stimp {stimp} green with a {slope}% slope:")

distance, seconds = calculate(degrees, stimp)
print("Went up %f feet (%f) in %f seconds" % (distance, distance-stimp, seconds))

distance, seconds = calculate(-degrees, stimp)
print("Went down %f feet (+%f) in %f seconds" % (distance, distance-stimp, seconds))
