# Based on turtle.py, a Tkinter based turtle graphics module for Python
# Version 1.1b - 4. 5. 2009
# Copyright (C) 2006 - 2010  Gregor Lingl
# email: glingl@aon.at
#
# The MIT License (MIT)
#
# Copyright (c) 2019 LadyAda and Dave Astels for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_turtle`
================================================================================

* Originals Author(s): LadyAda and Dave Astels

Implementation Notes
--------------------

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

#pylint:disable=too-many-public-methods, too-many-instance-attributes, invalid-name
#pylint:disable=too-few-public-methods, too-many-lines, too-many-arguments

import gc
import math
import time
import board
import displayio
#import adafruit_logging as logging

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_turtle.git"

class Color(object):
    """Standard colors"""
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    RED = 0xFF0000
    ORANGE = 0xFFA500
    YELLOW = 0xFFEE00
    GREEN = 0x00C000
    BLUE = 0x0000FF
    PURPLE = 0x8040C0
    PINK = 0xFF40C0

    colors = (BLACK, WHITE, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK)

    def __init__(self):
        pass


class Vec2D(tuple):
    """A 2 dimensional vector class, used as a helper class
    for implementing turtle graphics.
    May be useful for turtle graphics programs also.
    Derived from tuple, so a vector is a tuple!
    """
    # Provides (for a, b vectors, k number):
    #     a+b vector addition
    #     a-b vector subtraction
    #     a*b inner product
    #     k*a and a*k multiplication with scalar
    #     |a| absolute value of a
    #     a.rotate(angle) rotation
    def __init__(self, x, y):
        super(Vec2D, self).__init__((x, y))

    def __add__(self, other):
        return Vec2D(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0] * other[0]+self[1] * other[1]
        return Vec2D(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, (float, int)):
            return Vec2D(self[0] * other, self[1] * other)
        return None

    def __sub__(self, other):
        return Vec2D(self[0] - other[0], self[1] - other[1])

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __abs__(self):
        return (self[0]**2 + self[1]**2)**0.5

    def rotate(self, angle):
        """Rotate self counterclockwise by angle.

        :param angle: how much to rotate

        """
        perp = Vec2D(-self[1], self[0])
        angle = angle * math.pi / 180.0
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0] * c + perp[0] * s, self[1] * c + perp[1] * s)

    def __getnewargs__(self):
        return (self[0], self[1])

    def __repr__(self):
        return "({:.2f},{:.2f})".format(self[0], self[1])

class turtle(object):
    """A Turtle that can be given commands to draw."""

    def __init__(self, display=None, scale=1):
        if display:
            self._display = display
        else:
            try:
                self._display = board.DISPLAY
            except AttributeError:
                raise RuntimeError("No display available. One must be provided.")
        #self._logger = logging.getLogger("Turtle")
        #self._logger.setLevel(logging.INFO)
        self._w = self._display.width
        self._h = self._display.height
        self._x = self._w // 2
        self._y = self._h // 2
        self._speed = 6
        self._heading = 90
        self._logomode = False
        self._fullcircle = 360.0
        self._degreesPerAU = 1.0
        self._mode = "standard"
        self._angleOffset = 0
        self._bg_color = 0

        self._splash = displayio.Group(max_size=5)
        self._bgscale = 1
        if self._w == self._h:
            i = 1
            while self._bgscale == 1:
                if self._w/i < 128:
                    self._bg_bitmap = displayio.Bitmap(i, i, 1)
                    self._bgscale = self._w//i
                i += 1
        else:
            self._bgscale = self._GCD(self._w, self._h)
            self._bg_bitmap = displayio.Bitmap(self._w//self._bgscale, self._h//self._bgscale , 1)
        self._bg_palette = displayio.Palette(1)
        self._bg_palette[0] = Color.colors[self._bg_color]
        self._bg_sprite = displayio.TileGrid(self._bg_bitmap,
                                             pixel_shader=self._bg_palette,
                                             x=0, y=0)
        self._bg_group = displayio.Group(scale=self._bgscale,max_size=1)
        self._bg_group.append(self._bg_sprite)
        self._splash.append(self._bg_group)
        # group to add background pictures (and/or user-defined stuff)
        self._bg_addon_group = displayio.Group()
        self._splash.append(self._bg_addon_group)
        self._fg_scale = scale
        self._w = self._w // self._fg_scale
        self._h = self._h // self._fg_scale
        self._fg_bitmap = displayio.Bitmap(self._w, self._h, len(Color.colors))

        self._fg_palette = displayio.Palette(len(Color.colors))
        self._fg_palette.make_transparent(self._bg_color)
        for i, c in enumerate(Color.colors):
            self._fg_palette[i] = c
        self._fg_sprite = displayio.TileGrid(self._fg_bitmap,
                                             pixel_shader=self._fg_palette,
                                             x=0, y=0)
        self._fg_group = displayio.Group(scale=self._fg_scale, max_size=1)
        self._fg_group.append(self._fg_sprite)
        self._splash.append(self._fg_group)
        # group to add text and/or user defined stuff
        self._fg_addon_group = displayio.Group()
        self._splash.append(self._fg_addon_group)

        self._turtle_bitmap = displayio.Bitmap(9, 9, 2)
        self._turtle_palette = displayio.Palette(2)
        self._turtle_palette.make_transparent(0)

        self._turtle_palette[1] = Color.WHITE
        for i in range(4):
            self._turtle_bitmap[4 - i, i] = 1
            self._turtle_bitmap[i, 4 + i] = 1
            self._turtle_bitmap[4 + i, 7 - i] = 1
            self._turtle_bitmap[4 + i, i] = 1
        self._turtle_sprite = displayio.TileGrid(self._turtle_bitmap,
                                                 pixel_shader=self._turtle_palette,
                                                 x=-100, y=-100)
        self._drawturtle()
        self._turtle_group = displayio.Group(scale=self._fg_scale, max_size=1)
        self._turtle_group.append(self._turtle_sprite)
        self._splash.append(self._turtle_group)

        self._penstate = False
        self._pencolor = None
        self._pensize = 1
        self.pencolor(Color.WHITE)

        self._display.show(self._splash)
        gc.collect()

    def _drawturtle(self):
        self._turtle_sprite.x = int(self._x - 4)
        self._turtle_sprite.y = int(self._y - 4)
        #self._logger.debug("pos (%d, %d)", self._x, self._y)

    ############################################################################
    # Move and draw

    def forward(self, distance):
        """Move the turtle forward by the specified distance, in the direction the turtle is headed.

        :param distance: how far to move (integer or float)
        """
        p = self.pos()
        x1 = p[0] + math.sin(math.radians(self._heading)) * distance
        y1 = p[1] + math.cos(math.radians(self._heading)) * distance
        self.goto(x1, y1)
    fd = forward

    def backward(self, distance):
        """Move the turtle backward by distance, opposite to the direction the turtle is headed.
        Does not change the turtle's heading.

        :param distance: how far to move (integer or float)
        """

        self.forward(-distance)
    bk = backward
    back = backward

    def right(self, angle):
        """Turn turtle right by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on the turtle mode, see mode().

        :param angle: how much to rotate to the right (integer or float)
        """
        self._turn(angle)
    rt = right

    def left(self, angle):
        """Turn turtle left by angle units. (Units are by default degrees,
        but can be set via the degrees() and radians() functions.)
        Angle orientation depends on the turtle mode, see mode().

        :param angle: how much to rotate to the left (integer or float)
        """
        self._turn(-angle)
    lt = left

    #pylint:disable=too-many-branches,too-many-statements
    def goto(self, x1, y1=None):
        """If y1 is None, x1 must be a pair of coordinates or an (x, y) tuple

        Move turtle to an absolute position. If the pen is down, draw line.
        Does not change the turtle's orientation.

        :param x1: a number or a pair of numbers
        :param y1: a number or None
        """
        if y1 is None:
            y1 = x1[1]
            x1 = x1[0]
        x1 += self._w // 2
        y1 = self._h // 2 - y1
        x0 = self._x
        y0 = self._y
        #self._logger.debug("* GoTo from (%d, %d) to (%d, %d)", x0, y0, x1, y1)
        if not self.isdown():
            self._x = x1    # woot, we just skip ahead
            self._y = y1
            self._drawturtle()
            return
        steep = abs(y1 - y0) > abs(x1 - x0)
        rev = False
        dx = x1 - x0

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            dx = x1 - x0

        if x0 > x1:
            rev = True
            dx = x0 - x1

        dy = abs(y1 - y0)
        err = dx / 2
        ystep = -1
        if y0 < y1:
            ystep = 1
        step = 1
        ts = (((11-self._speed)*0.00020)*(self._speed+0.5))
        while (not rev and x0 <= x1) or (rev and x1 <= x0):
            if steep:
                try:
                    self._plot(int(y0), int(x0), self._pencolor)
                except IndexError:
                    pass
                self._x = y0
                self._y = x0
            else:
                try:
                    self._plot(int(x0), int(y0), self._pencolor)
                except IndexError:
                    pass
                self._x = x0
                self._y = y0
            if self._speed > 0:
                if step >= self._speed :
                    # mark the step
                    step = 1
                    self._drawturtle()
                    time.sleep(ts)
                else:
                    step += 1
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            if rev:
                x0 -= 1
            else:
                x0 += 1
        self._drawturtle()
    setpos = goto
    setposition = goto

    def setx(self, x):
        """Set the turtle's first coordinate to x, leave second coordinate
        unchanged.

        :param x: new value of the turtle's x coordinate (a number)

        """
        self.goto(x, self.pos()[1])

    def sety(self, y):
        """Set the turtle's second coordinate to y, leave first coordinate
        unchanged.

        :param y: new value of the turtle's y coordinate (a number)

        """
        self.goto(self.pos()[0], y)

    def setheading(self, to_angle):
        """Set the orientation of the turtle to to_angle. Here are some common
        directions in degrees:

        standard mode | logo mode
        0 - east | 0 - north
        90 - north | 90 - east
        180 - west | 180 - south
        270 - south | 270 - west

        :param to_angle: the new turtle heading

        """

        self._heading = to_angle
    seth = setheading

    def home(self):
        """Move turtle to the origin - coordinates (0,0) - and set its heading to
        its start-orientation
        (which depends on the mode, see mode()).
        """
        self.setheading(90)
        self.goto(0, 0)

    def _plot(self, x, y, c):
        if self._pensize == 1:
            self._fg_bitmap[int(x), int(y)] = c
            return
        offset = 0
        if self._pensize > 2:
            if self._pensize % 2 == 0:
                offset = (self._pensize//2)-1
            else:
                offset = (self._pensize-1)//2
        if 45 < self._heading < 135 or 225 < self._heading < 315:
            j = 1
            if 225 < self._heading :
                j = -1
            for i in range(0-offset,self._pensize-offset):
                try:
                    self._fg_bitmap[int(x)+i*j, int(y)] = c
                except IndexError:
                    pass
        else:
            j = 1
            if 135 < self._heading < 225:
                j = -1
            for i in range(0-offset,self._pensize-offset):
                try:
                    self._fg_bitmap[int(x), int(y)+i*j] = c
                except IndexError:
                    pass

    def circle(self, radius, extent=None, steps=None):
        """Draw a circle with given radius. The center is radius units left of
        the turtle; extent - an angle - determines which part of the circle is
        drawn. If extent is not given, draw the entire circle. If extent is not
        a full circle, one endpoint of the arc is the current pen position.
        Draw the arc in counterclockwise direction if radius is positive,
        otherwise in clockwise direction. Finally the direction of the turtle
        is changed by the amount of extent.

        As the circle is approximated by an inscribed regular polygon, steps
        determines the number of steps to use. If not given, it will be
        calculated automatically. May be used to draw regular polygons.

        :param radius: the radius of the circle
        :param extent: the arc of the circle to be drawn
        :param steps: how many points along the arc are computed
        """
        # call: circle(radius)                  # full circle
        # --or: circle(radius, extent)          # arc
        # --or: circle(radius, extent, steps)
        # --or: circle(radius, steps=6)         # 6-sided polygon

        if extent is None:
            extent = self._fullcircle
        if steps is None:
            frac = abs(extent)/self._fullcircle
            steps = 1+int(min(11+abs(radius)/6.0, 59.0)*frac)
        w = 1.0 * extent / steps
        w2 = 0.5 * w
        l = 2.0 * radius * math.sin(w2*math.pi/180.0*self._degreesPerAU)
        if radius < 0:
            l, w, w2 = -l, -w, -w2
        self.left(w2)
        for _ in range(steps):
            self.forward(l)
            self.left(w)
        self.right(w2)

    def _draw_disk(self, x, y, width, height, r, color, fill=True, outline=True, stroke=1):
        """Draw a filled and/or outlined circle"""
        if fill:
            self._helper(x+r, y+r, r, color=color, fill=True,
                         x_offset=width-2*r-1, y_offset=height-2*r-1)
        if outline:
            self._helper(x+r, y+r, r, color=color, stroke=stroke,
                         x_offset=width-2*r-1, y_offset=height-2*r-1)

    def speed(self, speed=None):
        """

        Set the turtle's speed to an integer value in the range 0..10. If no
        argument is given, return current speed.

        If input is a number greater than 10 or smaller than 1, speed is set
        to 0. Speedstrings are mapped to speedvalues as follows:

        "fastest": 0
        "fast": 10
        "normal": 6
        "slow": 3
        "slowest": 1
        Speeds from 1 to 10 enforce increasingly faster animation of line
        drawing and turtle turning.

        Attention: speed = 0 means that no animation takes place.
        forward/back makes turtle jump and likewise left/right make the
        turtle turn instantly.

        :param speed: the new turtle speed (0..10) or None
        """
        if speed == None:
            return self._speed
        elif speed > 10 or speed < 1:
            self._speed = 0
        else:
            self._speed = speed

  # pylint: disable=too-many-locals, too-many-branches
    def _helper(self, x0, y0, r, color, x_offset=0, y_offset=0,
                stroke=1, fill=False):
        """Draw quandrant wedges filled or outlined"""
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = -1
        y = r

        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            if fill:
                for w in range(x0-y, x0+y+x_offset):
                    self._plot(w, y0 + x + y_offset, color)
                    self._plot(w, y0 - x, color)
                for w in range(x0-x, x0+x+x_offset):
                    self._plot(w, y0 + y + y_offset, color)
                    self._plot(w, y0 - y, color)
            else:
                for line in range(stroke):
                    self._plot(x0 - y + line, y0 + x + y_offset, color)
                    self._plot(x0 - x, y0 + y + y_offset - line, color)
                    self._plot(x0 - y + line, y0 - x, color)
                    self._plot(x0 - x, y0 - y + line, color)
            for line in range(stroke):
                self._plot(x0 + x + x_offset, y0 + y + y_offset - line, color)
                self._plot(x0 + y + x_offset - line, y0 + x + y_offset, color)
                self._plot(x0 + x + x_offset, y0 - y + line, color)
                self._plot(x0 + y + x_offset - line, y0 - x, color)

    # pylint: enable=too-many-locals, too-many-branches

#pylint:disable=keyword-arg-before-vararg
    def dot(self, size=None, color=None):
        """Draw a circular dot with diameter size, using color.
        If size is not given, the maximum of pensize+4 and
        2*pensize is used.

        :param size: the diameter of the dot
        :param color: the color of the dot

        """
        if size is None:
            size = max(self._pensize + 4, self._pensize * 2)
        if color is None:
            color = self._pencolor
        else:
            color = self._color_to_pencolor(color)
        #self._logger.debug('dot(%d)', size)
        self._draw_disk(self._x - size, self._y - size, 2 * size + 1, 2 * size + 1, size, color)
        self._fg_sprite[0, 0] = 0


    ############################################################################
    # Tell turtle's state

    def pos(self):
        """Return the turtle's current location (x,y) (as a Vec2D vector)."""
        return Vec2D(self._x - self._w // 2, self._h // 2 - self._y)
    position = pos

    def xcor(self):
        """Return the turtle's x coordinate."""
        return self._x - self._w // 2

    def ycor(self):
        """Return the turtle's y coordinate."""
        return self._h // 2 - self._y

    def heading(self):
        """Return the turtle's current heading (value depends on the turtle
        mode, see mode()).
        """
        return self._heading



    ############################################################################
    # Setting and measurement

    def _setDegreesPerAU(self, fullcircle):
        """Helper function for degrees() and radians()"""
        self._fullcircle = fullcircle
        self._degreesPerAU = 360/fullcircle
        if self._mode == "standard":
            self._angleOffset = 0
        else:
            self._angleOffset = fullcircle/4.


    def degrees(self, fullcircle=360):
        """Set angle measurement units, i.e. set number of "degrees" for a full circle.
        Default value is 360 degrees.

        :param fullcircle: the number of degrees in a full circle
        """
        self._setDegreesPerAU(fullcircle)

    def radians(self):
        """Set the angle measurement units to radians. Equivalent to degrees(2*math.pi)."""
        self._setDegreesPerAU(2*math.pi)


    ############################################################################
    # Drawing state

    def pendown(self):
        """Pull the pen down - drawing when moving."""
        self._penstate = True
    pd = pendown
    down = pendown

    def penup(self):
        """Pull the pen up - no drawing when moving."""
        self._penstate = False
    pu = penup
    up = penup

    def pensize(self, width=None):
        """

        Set the line thickness to width or return it. If resizemode is set to
        "auto" and turtleshape is a polygon, that polygon is drawn with the same
        line thickness. If no argument is given, the current pensize is returned.

        :param width: - a positive number

        """
        if width is not None:
            self._pensize = width
        return self._pensize
    width = pensize

    def isdown(self):
        """Return True if pen is down, False if it's up."""
        return self._penstate

    ############################################################################
    # Color control

#pylint:disable=no-self-use
    def _color_to_pencolor(self, c):
        return Color.colors.index(c)


    def pencolor(self, c=None):
        """
        Return or set the pencolor.

        pencolor()
            Return the current pencolor as color specification string or as a
            tuple (see example). May be used as input to another color/
            pencolor/fillcolor call.

        pencolor(colorvalue)
            Set pencolor to colorvalue, which is a 24-bit integer such as 0xFF0000.
            The Color class provides the available values:
            WHITE, BLACK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK
        """
        if c is None:
            return Color.colors[self._pencolor]
        if not c in Color.colors:
            raise RuntimeError("Color must be one of the 'Color' class items")
        self._pencolor = Color.colors.index(c)
        self._turtle_palette[1] = c
        if self._bg_color == self._pencolor:
            self._turtle_palette.make_transparent(1)
        else:
            self._turtle_palette.make_opaque(1)
        return c

    def bgcolor(self, c=None):
        """
        Return or set the background color.

        bgcolor()
            Return the current backgroud color as color specification string.
            May be used as input to another color/ pencolor/fillcolor call.

        bgcolor(colorvalue)
            Set backgroud color to colorvalue, which is a 24-bit integer such as 0xFF0000.
            The Color class provides the available values:
            WHITE, BLACK, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK
        """
        if c is None:
            return Color.colors[self._bg_color]
        if not c in Color.colors:
            raise RuntimeError("Color must be one of the 'Color' class items")
        old_color = self._bg_color
        self._fg_palette.make_opaque(old_color)
        self._bg_color = Color.colors.index(c)
        self._bg_palette[0] = c
        self._fg_palette.make_transparent(self._bg_color)
        self._turtle_palette[0] = c
        if self._bg_color == self._pencolor:
            self._turtle_palette.make_transparent(1)
        else:
            self._turtle_palette.make_opaque(1)
        for h in range(self._h):
            for w in range(self._w):
                if self._fg_bitmap[w, h] == old_color :
                    self._fg_bitmap[w, h] = self._bg_color


    def set_bgpic(self, file):
        """
        Set a picture as background.

        set_bgpic(filename)
            Set backgroud picture using OnDiskBitmap.
        """
        self._bg_pic = open(file, 'rb')
        odb = displayio.OnDiskBitmap(self._bg_pic)
        self._odb_tilegrid = displayio.TileGrid(odb, pixel_shader=displayio.ColorConverter())
        self._bg_addon_group.append(self._odb_tilegrid)
        #centered
        # ALFA test
        self._odb_tilegrid.y = ((self._h*self._fg_scale)//2) - (odb.height//2)
        self._odb_tilegrid.x = ((self._w*self._fg_scale)//2) - (odb.width//2)

        #self._odb_tilegrid.y = (self._h//2) - (odb.height//2)
        #self._odb_tilegrid.x = (self._w//2) - (odb.width//2)

    def del_bgpic(self):
        """
        Remove the background picture, if any

        del_bgpic()
            Remove the picture and close the file
        """
        if self._bg_pic != None:
            self._bg_addon_group.remove(self._odb_tilegrid)
            self._odb_tilegrid = None
            self._bg_pic.close()
            self._bg_pic = None




    ############################################################################
    # More drawing control

    def clear(self):
        """Delete the turtle's drawings from the screen. Do not move turtle."""
        for w in range(self._w):
            for h in range(self._h):
                self._fg_bitmap[w, h] = self._bg_color
        for i, c in enumerate(Color.colors):
            self._fg_palette[i] = c ^ 0xFFFFFF
        for i, c in enumerate(Color.colors):
            self._fg_palette[i] = c
        time.sleep(0.1)

    ############################################################################
    # Other

    def _turn(self, angle):
        if self._logomode:
            self._heading -= angle
        else:
            self._heading += angle
        self._heading %= 360         # wrap


    def _GCD(self, a, b):
        """GCD(a,b):
        english : recursive 'Greatest common divisor' calculus for int numbers a and b"""
        if b==0:
            return a
        else:
            r=a%b
            return self._GCD(b,r)
