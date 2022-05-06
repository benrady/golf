import stimpmeter

def ratio(slope, stimp):
    if slope == 0:
        return round(100 * 10.0 / stimp)
     # Should be the same as the stimp, but we're correcting for error
    flat_distance, _ = stimpmeter.calculate(0, stimp)

    distance, _ = stimpmeter.calculate(slope, stimp)
    if distance is None:
        return 0
    return round((10 * 100 * flat_distance) / (distance * stimp))

print("8,9,10,11")
for slope in range(7, -8, -1):
    line = f"{slope}"
    for stimp in range(8, 12):
        line += f",{ratio(slope, stimp)}"
    print(line)
