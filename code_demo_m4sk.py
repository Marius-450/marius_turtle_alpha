
# Code to demonstrate improvements of marius_turtle (to be added to adafruit_turtle)
# Retro-compatible by try and except.
# Code for the Circuit playground with TFT_GIZMO

import time
import board

import digitalio
import busio
import displayio

import gc
import os
from random import randint


from marius_turtle import Color, turtle

#from adafruit_turtle import Color, turtle


from adafruit_st7789 import ST7789
from adafruit_seesaw.seesaw import Seesaw


i2c = busio.I2C(board.SCL, board.SDA)
# backlight left display pin initialisation via seesaw
ss = Seesaw(i2c)
ss.pin_mode(5, ss.OUTPUT)

# display setup for m4sk
displayio.release_displays()

spi1 = busio.SPI(board.RIGHT_TFT_SCK, MOSI=board.RIGHT_TFT_MOSI)
display1_bus = displayio.FourWire(spi1, command=board.RIGHT_TFT_DC, chip_select=board.RIGHT_TFT_CS, reset=board.RIGHT_TFT_RST)
display1 = ST7789(display1_bus, width=240, height=240, rowstart=80, backlight_pin=board.RIGHT_TFT_LITE)

spi2 = busio.SPI(board.LEFT_TFT_SCK, MOSI=board.LEFT_TFT_MOSI)
display2_bus = displayio.FourWire(spi2, command=board.LEFT_TFT_DC, chip_select=board.LEFT_TFT_CS)
display2 = ST7789(display2_bus, width=240, height=240, rowstart=80)


# backlight left display on
ss.analog_write(5, 255)


# to use 2 times less memory, use only 4 colors.
#Color.colors = Color.colors[:4]
# to use 4 times less memory, use only 2 colors.
#Color.colors = Color.colors[:2]

gc.collect()
mem_before = gc.mem_alloc()

# to use 4 time less memory, use scale=2
#turtle1 = turtle(display2, scale=2)
turtle1 = turtle(display2)

print("Memory used by turtle object :",gc.mem_alloc() - mem_before)
# Loop forever

turtle1.penup()
turtle1.goto(turtle1._w//2-10,turtle1._h//2-10)

color_choice = 1
turtle1.pendown()
turtle1.setheading(0)
turtle1.pensize(1)

sizes = [1,2,3,5,11,19]
# not available yet
s = 0


while True:
    if s % 2 == 0:
        try:
            turtle1.set_bgpic("/blinka_dark.bmp")
        except:
            pass
        try:
            turtle1.changeturtle()
        except:
            pass
    else:
        try:
            turtle1.changeturtle("/turtle.bmp")
        except:
            pass
    turtle1.pensize(sizes[s])
    s += 1
    if s >= len(sizes):
        s = 0
    try:
        turtle1.bgcolor(Color.colors[randint(0,len(Color.colors)-1)])
        print("bg_color", turtle1._bg_color, "size", turtle1.pensize())
        color_choice = turtle1._bg_color + 1
        if color_choice >= len(Color.colors):
            color_choice = 0
    except:
        print("size", turtle1.pensize())

    turtle1.pencolor(Color.colors[color_choice])
    for speed in range(0,12):
        try:
            turtle1.speed(speed)
        except:
            pass
        start_time = time.monotonic()
        for i in range(1,6):
            turtle1.setheading(270)
            turtle1.goto(turtle1._w//2-10,-(turtle1._h//2-10))
            turtle1.setheading(180)
            turtle1.goto(-(turtle1._w//2-10),-(turtle1._h//2-10))
            turtle1.setheading(90)
            turtle1.goto(-(turtle1._w//2-10),turtle1._h//2-10)
            turtle1.setheading(0)
            turtle1.goto(turtle1._w//2-10,turtle1._h//2-10)
            try:
                turtle1.pencolor(Color.colors[turtle1._bg_color])
            except:
                turtle1.pencolor(Color.BLACK)
            turtle1.setheading(270)
            turtle1.goto(turtle1._w//2-10,-(turtle1._h//2-10))
            turtle1.setheading(180)
            turtle1.goto(-(turtle1._w//2-10),-(turtle1._h//2-10))
            turtle1.setheading(90)
            turtle1.goto(-(turtle1._w//2-10),turtle1._h//2-10)
            turtle1.setheading(0)
            turtle1.goto(turtle1._w//2-10,turtle1._h//2-10)
            color_choice += 1
            try:
                if color_choice >= len(Color.colors):
                    color_choice = 0
                if color_choice == turtle1._bg_color:
                    color_choice += 1
                    if color_choice >= len(Color.colors):
                        color_choice = 0
            except:
                if color_choice >= len(Color.colors):
                    color_choice = 1

            turtle1.pencolor(Color.colors[color_choice])
        try:
            print("speed", turtle1.speed() ,":", time.monotonic() - start_time, "sec")
        except:
            print(time.monotonic() - start_time, "sec")
        time.sleep(2)
    try:
        turtle1.del_bgpic()
    except:
        pass

