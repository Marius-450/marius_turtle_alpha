# marius_turtle_alpha
dev repo for improvements of adafruit_turtle lib. demo code for Monster M4sk and Circuit Playground + TFT Gizmo


## What's new ?

### Colors
* changed green, pink, purple, values. 
* put black at the first place, as the color 0 is the default color for the background.
* Black was redondant in the `_fg_palette`, this permit to add a 16th color before doubling the memory used by `_fg_bitmap`
* Added 7 colors as 16 consume the same memory as 5 or 9.
* added `bgcolor()` method to set and get background color.
* when used, the default turtle shape change color when changing pen color.

### Memory
* divided the memory used for the background bitmap (around 7200 Bytes saved for 240x240). It draw the tiniest bitmap that can be scaled to full screen for any display shape.
* turtle object have a new `scale` parameter (default : 1), that divide the memory used by the foreground bitmap by the square of the scale value. It also divide height and width by this value, and each pixel drawn on the bitmap is rendered by `scale`^2 pixels on the screen. (for 240x240 display and colors between 5 and 16 : scale = 1 -> 28800 Bytes, scale = 2 -> 7200 Bytes)

### Other
* added `pensize()` method to set and get the pen size. Works with goto, and rotate. At any angle, the thickness stay the same.
* added `speed()` method to set and get the speed of the drawing. default is 6. 1 is slowest, 10 is fast, 0 is "instantaneous" or "the faster you can get" dependant of the pen size.
* added `set_bgpic()` and `del_bgpic()` methods to set and remove a background picture, using OnDiskBitmap
* added two intermediary groups
  * between background and foreground (`_bg_addon_group`) for background images, (in the future) stamps, or user defined stuff
  * between foreground and turtle  (`_fg_addon_group`) for writing text (also in the future), or for user defined stuff
* added `mode()` method to switch between logo and standard modes. logo mode is the default (it was, in reality).
* added `towards()` method. return the heading angle toward a point. (*idea: gotoward() that do setheading(towards(x,y)) and goto(x,y)*)
* added `turtleshow()`, `turtlehide()` and `isvisible()` methods to hide and show the turtle, and know the state of visibility.
* added `changeturtle()` method. Accepts 3 possibilities :
  * No argument : go back to the default shape. if an image file is still open, closes it.
  * a string with a path to an image : use OnDiskBitmap to load the image and replace the turtle shape.
  * a TileGrid object and a tupple with the dimensions : replace the turtle shape by the Tilegrid object, the tuple must contain the width and height of the bitmap.
* added `distance()` method. Return the distance to a point.
* added `window_height()` and `window_width()` methods to return display dimensions



