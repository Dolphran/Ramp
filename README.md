# Ramp
Calculations for constructing a parabolic ramp. (as for RC cars)

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
