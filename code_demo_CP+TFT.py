
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


from adafruit_gizmo import tft_gizmo

from marius_turtle import Color, turtle

#from adafruit_turtle import Color, turtle


displayio.release_displays()
# Create the TFT Gizmo display
display2 = tft_gizmo.TFT_Gizmo()



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
turtle1.setheading(90)
turtle1.pensize(1)

sizes = [1,2,3,5,11,19]
# not available yet
s = 0

while True:
    if s % 2 == 0:
        try:
            turtle1.bgpic("/blinka_dark.bmp")
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
            turtle1.right(90)
            turtle1.forward(turtle1._h-20)
            turtle1.right(90)
            turtle1.forward(turtle1._w-20)
            turtle1.right(90)
            turtle1.forward(turtle1._h-20)
            turtle1.right(90)
            turtle1.forward(turtle1._w-20)
            try:
                turtle1.pencolor(Color.colors[turtle1._bg_color])
            except:
                turtle1.pencolor(Color.BLACK)
            turtle1.right(90)
            turtle1.forward(turtle1._h-20)
            turtle1.right(90)
            turtle1.forward(turtle1._w-20)
            turtle1.right(90)
            turtle1.forward(turtle1._h-20)
            turtle1.right(90)
            turtle1.forward(turtle1._w-20)
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
        turtle1.bgpic("nopic")
    except:
        pass

