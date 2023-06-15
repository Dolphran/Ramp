"""
This script is for calculating and displaying dimensions useful for constructing a parabolic ramp.
The script will take as input any two of the following for values defining the ramp
* The horizontal length of the ramp
* The height of the ramp
* The exit angle of the ramp
* The length of the curved surface of the ramp

Some details:

We may remember from high school algebra that all parabolas are defined by the equation y = ax^2 + bx + c.
For our purposes, the values of b and c can be considered to be 0, because their only effect is to move
the parabola in 2d space (as on graph paper) so that it doesn't start at the point (0,0).
But the actual shape of the parabola is determined by the value of a.
For parabolas that curve upward, 'a' will be greater than zero. 'a' values less than 1 will yeild
fat parabolas and values greater that 1 will yeild skinny parabolas.

This script is for a ramp that follows the curve y = x^2,
which means 'a' is 1 (and the parabola is neither fat nor skinny!)

But knowing that we want the shape y = x^2 doesn't directly help us when we want to construct a ramp that is
measured in inches or millimeters (or any unit of measurement that we want to use for constructing the ramp)
The actual numerical values in our desired units are scaled from the values that the equation y = x^2 yields.
This scaling is needed both to show the values in prefered units and to make bigger or smaller ramps
that still follow the parabolic curve defined by y = x^2.

So we need to determine this scale factor for our ramp in our desired units of measurment.
Mathmatically, we can say that for a given horizontal length, 'l', and vertcal height, 'h', of any point on the
ramp (in any unit of measurment), there exists a scale factor, 's', where y = (h/s), x = (l/s), and y = x^2.
So we get a scale factor, 's' where h/s = (l/s)^2 for that physical ramp size in those units. 
With algebraic substitution we can see that (h/s) = l^2 / s^2, and multiplying both sides by 's' gives h = l^2/s
and so s = l^2/h. This can be restated that for any point on the ramp surface in any units,
we can take the (hotizontal) length and height of that point and get the scale factor for that ramp:

scale_factor = length * length / height.

If we know the overall and length and height we want the ramp to be we can now easily determine the scale factor.
And we can now determine the height of the ramp at any length interval, (say, for example, every 4 inches across).
This could be used to physically mark points that will define the curve of the ramp for physical construction.

However, when wanting to construct a ramp, you may not know, initially, the overall length and height. Instead,
you may know that you want the end of the ramp to be 2 feet high, and that it should be pointing upward at
a 45 degree angle at the end of the ramp (we'll call this the "exit angle"). Or, you may know how long
the curved surface of the ramp will be (becasue you have that length of material to construct it), and
the exit angle you want, and you want to determine the (horizontal) length and height based on those values.

So there are really four different values we may want to take into consideration in constructing the ramp.
* The horizontal length of the ramp
* The height of the ramp
* The exit angle of the ramp
* The length of the curved surface of the ramp
If we define ANY TWO of the above values, we can determine exactly the values of the other two.
And by defintion we then know the scale factor of that particular ramp.
As described earlier, we can then use the scale factor to easily list the height of the ramp
along any length interval. That is exactly what this script does.
"""

import math
from ast import literal_eval

def point_at_angle_on_parabola(angle):
    # Convert the angle from degrees to radians
    theta = math.radians(angle)
    # Calculate the x-coordinate using the tangent of the angle
    x = math.tan(theta) / 2
    # Calculate the y-coordinate using the equation of the parabola
    y = x**2
    return x, y

def angle_at_point_on_parabola(x):
    # for parabola y = x**2
    slope = 2 * x
    return math.degrees(math.atan(slope))

def parabolic_arc_length(x):
    # Function to calculate the arc length of y=x**2 from 0 to x
    h = x**2
    w = 2 * x
    i0 = math.sqrt(w**2 + 16 * h**2)
    i1 = 1/2 * i0
    i2 = w**2 / (8 * h) * math.log((4 * h + i0) / w)
    arc_length = (i1 + i2) / 2
    return arc_length

def point_at_arc_length_on_parabola(arc_length, epsilon=0.0000001):
    x_min = 0
    x_max = arc_length  # Set an upper limit for x

    while x_max - x_min > epsilon:
        x_mid = (x_min + x_max) / 2
        calculated_arc_length = parabolic_arc_length(x_mid)

        if abs(calculated_arc_length - arc_length) < epsilon:
            return x_mid

        if calculated_arc_length < arc_length:
            x_min = x_mid
        else:
            x_max = x_mid

    return (x_min + x_max) / 2

def find_scale_factor_from_ramp_surface_length_and_horizontal_length(r, l, epsilon=0.0000001):
    s_min = 1.0  # Minimum value of s
    s_max = 10000.0  # Maximum value of s
    
    while abs(s_max - s_min) > epsilon:
        s_mid = (s_min + s_max) / 2.0  # Calculate the midpoint
        
        if point_at_arc_length_on_parabola(r/s_mid, epsilon) > l/s_mid:
            s_max = s_mid
        else:
            s_min = s_mid
    
    s = (s_min + s_max) / 2.0  # Calculate the final s value
    
    return s

def find_scale_factor_from_ramp_surface_length_and_height(r, h, epsilon=0.0000001):
    s_min = 1.0  # Minimum value of s
    s_max = 10000.0  # Maximum value of s
    
    while abs(s_max - s_min) > epsilon:
        s_mid = (s_min + s_max) / 2.0  # Calculate the midpoint
        
        flip = (h / s_mid) < 1 # because the square root of this is larger than the original value
        if point_at_arc_length_on_parabola(r/s_mid, epsilon) > math.sqrt(h/s_mid):
            if not flip : s_max = s_mid
            else : s_min = s_mid
        else:
            if not flip : s_min = s_mid
            else : s_max = s_mid
   
    s = (s_min + s_max) / 2.0  # Calculate the final s value
    
    return s

def nearest_fraction(value, frac):
    if (frac <= 0) :
        return f"{value:.{-frac}f}" 
    whole_number = int(value)
    fraction = value - whole_number
    # Convert fractional part to nearest fraction (for nearest 16th, frac would be 16)
    numerator = round(fraction * frac)
    denominator = frac
    if (numerator == 0) :
        return f"{whole_number}"
    # Simplify fraction if possible
    while numerator % 2 == 0:
        numerator //= 2
        denominator //= 2
    if (denominator == 1) :
        return f"{whole_number + numerator}"
    return f"{whole_number}-{numerator}/{denominator}"

def calculate_unknowns(exit_angle, ramp_length, length, height, do_print = False, frac = None) :
    # This routine assumes that of the first four arguments, only two will be defined (the other two will be 'None')
    if exit_angle is not None :
        x, y = point_at_angle_on_parabola(exit_angle)
        arc_length = parabolic_arc_length(x)
        if ramp_length is not None :
            if do_print : print(f"\nFor parabolic ramp with exit angle = {exit_angle} degrees and ramp surface length = {ramp_length}")
            scale_factor = ramp_length / arc_length
            length = x * scale_factor
            height = y * scale_factor
            if do_print : print(f"The total horizontal length = {nearest_fraction(length, frac)} and the total height = {nearest_fraction(height, frac)}")
        elif length is not None :
            if do_print : print(f"\nFor parabolic ramp with exit angle = {exit_angle} and horizontal length = {length}")
            scale_factor = length / x
            ramp_length = arc_length * scale_factor
            height = y * scale_factor
            if do_print : print(f"The ramp surface length = {nearest_fraction(ramp_length, frac)} and the total height = {nearest_fraction(height, frac)}")
        elif height is not None :
            if do_print : print(f"\nFor parabolic ramp with exit angle = {exit_angle} and vertical height = {height}")
            scale_factor = height / y
            ramp_length = arc_length * scale_factor
            length = x * scale_factor
            if do_print : print(f"The ramp surface length = {nearest_fraction(ramp_length, frac)} and horizontal length = {nearest_fraction(length, frac)}")
        else :
            print(f"Program logic Error.")
            exit()
    elif ramp_length is not None :
        if length is not None :
            if do_print : print(f"\nFor parabolic ramp with ramp surface length = {ramp_length} and horizontal length = {length}")
            scale_factor = find_scale_factor_from_ramp_surface_length_and_horizontal_length(ramp_length, length)
            height = (length / scale_factor)**2 * scale_factor
            exit_angle = angle_at_point_on_parabola(length / scale_factor)
            if do_print : print(f"The height = {nearest_fraction(height, frac)} and the exit angle = {exit_angle:.1f} degrees")
        else  :
            # We know here that height is not None
            if do_print : print(f"\nFor parabolic ramp with ramp surface length = {ramp_length} and vertical height = {height}")
            scale_factor = find_scale_factor_from_ramp_surface_length_and_height(ramp_length, height)
            length = math.sqrt(height / scale_factor) * scale_factor
            exit_angle = angle_at_point_on_parabola(length / scale_factor)
            if do_print : print(f"The horizontal length = {nearest_fraction(length, frac)} aand the exit angle = {exit_angle:.1f} degrees")
    else :
        if do_print : print(f"\nFor parabolic ramp with horizontal length = {length} and vertical height = {height}")
        scale_factor = length * length / height
        x = height / length # same as length / scale_factor
        arc_length  = parabolic_arc_length(x)
        assert (round(x * 10000) == round(point_at_arc_length_on_parabola(arc_length) * 10000)), f"{point_at_arc_length_on_parabola(arc_length)} is not close enought to {x}"
        y = x * x # same as height / scale_factor
        exit_angle = angle_at_point_on_parabola(x)
        ramp_length = arc_length * scale_factor
        if do_print : print(f"The ramp surface length = {nearest_fraction(ramp_length, frac)} and the exit angle = {exit_angle:.1f} degrees")

    return exit_angle, ramp_length, length, height, scale_factor

def test_ramp_values(exit_angle, ramp_length, length, height) :
    epsilon=0.001
    calc_exit_angle, calc_ramp_length, calc_length, calc_height, s = calculate_unknowns(exit_angle, ramp_length, None, None)
    assert (abs(calc_length - length) < epsilon), f"length {calc_length} is not close enought to {length}"
    assert (abs(calc_height - height) < epsilon), f"height {calc_height} is not close enought to {height}"
    calc_exit_angle, calc_ramp_length, calc_length, calc_height, s = calculate_unknowns(exit_angle, None, length, None)
    assert (abs(calc_ramp_length - ramp_length) < epsilon), f"{calc_ramp_length} is not close enought to {ramp_length}"
    assert (abs(calc_height - height) < epsilon), f"height {calc_height} is not close enought to {height}"
    calc_exit_angle, calc_ramp_length, calc_length, calc_height, s = calculate_unknowns(exit_angle, None, None, height)
    assert (abs(calc_ramp_length - ramp_length) < epsilon), f"{calc_ramp_length} is not close enought to {ramp_length}"
    assert (abs(calc_length - length) < epsilon), f"length {calc_length} is not close enought to {length}"
    calc_exit_angle, calc_ramp_length, calc_length, calc_height, s = calculate_unknowns(None, ramp_length, None, height)
    assert (abs(calc_exit_angle  - exit_angle) < epsilon), f"{calc_exit_angle} is not close enought to {exit_angle}"
    assert (abs(calc_length - length) < epsilon), f"length {calc_length} is not close enought to {length}"
    calc_exit_angle, calc_ramp_length, calc_length, calc_height, s = calculate_unknowns(None, ramp_length, length, None)
    assert (abs(calc_exit_angle  - exit_angle) < epsilon), f"{calc_exit_angle} is not close enought to {exit_angle}"
    assert (abs(calc_height - height) < epsilon), f"height {calc_height} is not close enought to {height}"
    calc_exit_angle, calc_ramp_length, calc_length, calc_height, s = calculate_unknowns(None, None, length, height)
    assert (abs(calc_exit_angle  - exit_angle) < epsilon), f"{calc_exit_angle} is not close enought to {exit_angle}"
    assert (abs(calc_ramp_length - ramp_length) < epsilon), f"{calc_ramp_length} is not close enought to {ramp_length}"


def print_ramp_points(ramp_length, scale_factor, coordinate_list_spacing, frac) :
    print(f"\nThe following lists the x-y coordinates of points along the ramp surface spaced every {coordinate_list_spacing}:")
    p = coordinate_list_spacing 
    while (p < ramp_length):
        arc_length = p / scale_factor
        locX = point_at_arc_length_on_parabola(arc_length)
        locY = locX * locX
        print(f"x = {nearest_fraction(scale_factor * locX, frac)}, y = {nearest_fraction(scale_factor * locY, frac)}, angle = {math.degrees(math.atan(2 * locX)):.1f}, ramp surface length = {nearest_fraction(parabolic_arc_length(locX) * scale_factor, frac)}")
        p += coordinate_list_spacing
    locX = length / scale_factor
    locY = locX * locX
    print(f"x = {nearest_fraction(scale_factor * locX, frac)}, y = {nearest_fraction(scale_factor * locY, frac)}, angle = {math.degrees(math.atan(2 * locX)):.1f}, ramp surface length = {nearest_fraction(parabolic_arc_length(locX) * scale_factor, frac)}")
    print()

# BEGIN MAIN SCRIPT

import sys
import argparse

# Define valid fraction values
VALID_FRACTIONS = [1, 2, 4, 8, 16, 32]

parser = argparse.ArgumentParser()

# Add command line arguments
parser.add_argument('-exit_angle', '-e', type=float, help="Exit angle in degrees")
parser.add_argument('-ramp_surface_length', '-r', type=float, help="Ramp surface length")
parser.add_argument('-length', '-l', type=float, help="Horizontal Length")
parser.add_argument('-height', '-t', type=float, help="Height at end of ramp")
parser.add_argument('-fraction', '-f', type=int, help="Nearest Fractional value for dimension output (e.g. 8 means nearest eighth)")
parser.add_argument('-decimal', '-d', type=int, help="Number of Decimal places for dimension output (if fraction not specified)")
parser.add_argument('-list_spacing', '-s', type=int, help="Coordinate list spacing along ramp surface")

# Parse the command line arguments
args = parser.parse_args()

# Process the arguments
exit_angle = args.exit_angle
ramp_length = args.ramp_surface_length
length = args.length
height = args.height
fraction = args.fraction
decimal = args.decimal
coordinate_list_spacing = args.list_spacing

# Validate the arguments
specified_args = [arg is not None for arg in [exit_angle, ramp_length, length, height]]
if specified_args.count(True) != 2:
    print("Error: You must specify exactly two of the following arguments: -e, -r, -l, -t")
    parser.print_help()
    exit(1)

if not all(arg is None or arg > 0 for arg in [exit_angle, ramp_length, length, height, fraction, coordinate_list_spacing]):
    print("Error: All arguments must be positive non-zero numeric values.")
    parser.print_help()
    exit(1)

if fraction and decimal:
    print("Error: -f and -d cannot both be specified.")
    parser.print_help()
    exit(1)

if fraction is not None and fraction not in VALID_FRACTIONS:
    print("Error: -f can only have the values 2, 4, 8, 16, or 32.")
    parser.print_help()
    exit(1)

if exit_angle and exit_angle >= 90:
    print("Error: Exit angle must be less than 90.")
    parser.print_help()
    exit(1)

if not fraction and not decimal:
    frac = 1
elif not fraction :
    frac = -decimal
else :
    frac = fraction

if not coordinate_list_spacing:
    coordinate_list_spacing = 4

"""
print("Exit Angle:", exit_angle)
print("Ramp Surface Length:", ramp_length)
print("Length:", length)
print("Height:", height)
print("Fraction:", fraction)
print("Decimal:", decimal)
print("Coordinate List Interval:", coordinate_list_spacing)
"""
exit_angle, ramp_length, length, height, scale_factor = calculate_unknowns(exit_angle, ramp_length, length, height, True, frac)

test_ramp_values(exit_angle, ramp_length, length, height)

print_ramp_points(ramp_length, scale_factor, coordinate_list_spacing, frac)