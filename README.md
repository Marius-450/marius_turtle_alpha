# marius_turtle_alpha
Dev repo for improvements of adafruit_turtle lib. <br />
Demo code for Monster M4sk and Circuit Playground + TFT Gizmo<br />

Lib fully (upward) compatible with adafruit_turtle. Running code written for adafruit_turtle with marius_turtle will make it slower, as the first don't manage speed at all, and that default to speed 6 now.<br />
Tested with published code for adafruit_turtle. 
One change will be needed in 4 examples : adding `turtle.setheading(90)`  as the default heading is now 0, meaning heading North for logo mode (default), and East for standart mode

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

### Logo mode vs Standard mode
I noticed the default mode was not consistent with the documentation. Default heading was toward East, but East was 90 instead of 0 and the directions heading were those of logo mode.

* `mode()` method now implemented and consistent with documentation
* default mode is "logo"
* default heading is 0 : East for "standard", North for "logo"


### Other
* Added `pensize()` method to set and get the pen size. Works with goto, and rotate. At any angle, the thickness stay the same.
* Added `speed()` method to set and get the speed of the drawing. default is 6. 1 is slowest, 10 is fast, 0 is "instantaneous" or "the faster you can get" dependant of the pen size.
* Added `bgpic()` method to set and remove a background picture, using OnDiskBitmap
  * `bgpic()` return the background picture filename, if any.
  * `bgpic("nopic")` remove the picture from background.
  * `bgpic(filename)` set a picture as background.
* Added two intermediary groups
  * between background and foreground (`_bg_addon_group`) for background images or user defined stuff
  * between foreground and turtle  (`_fg_addon_group`) for writing text (in the future), stamps, or for user defined stuff
* Added `towards()` method. return the heading angle toward a point.
* Added `turtleshow()`, `turtlehide()` and `isvisible()` methods to hide and show the turtle, and know the state of visibility.
* Added `changeturtle()` method. Accepts 3 possibilities :
  * No argument : go back to the default shape. if an image file is still open, closes it.
  * a string with a path to an image : use OnDiskBitmap to load the image and replace the turtle shape.
  * a TileGrid object and a tupple with the dimensions : replace the turtle shape by the Tilegrid object, the tuple must contain the width and height of the bitmap (default = (12,12) ). This value is only used to center the bitmap correctly.
* Added `distance()` method. Return the distance to a point.
* Added `window_height()` and `window_width()` methods to return display dimensions
* Fixed some rounding error accumulating in `circle()` process. Last step make sure the heading and position are the same as starting heading and position.
* Added `stamp()`, `clearstamp()` and `clearstamps()` methods to stamp the turtle shape on the canvas and remove those stamps.
* Added `reset()` method to erase all drawings and reset the turtle to default parameters and position
* Simplified `dot()` to use turn instead of 2 helper methods. the first arg is now the diameter instead of radius, to be consistent with the documentation. Resulting dot is rounder.

## TODO

* write text
* pen dict : get or set multiple parameters at once
* polygons
* filling shapes
* getcanvas : something like a screenshot.

## To be discarded

* event-based methods (onclick, onrelease etc.) There is no mouse, and no event management user side.
* undo buffer : no use case come to mind. much complexification, increased memory use, with few to no benefits at all.
* tilt angle and sheer factor : Can't see a way to fully implement that. rotation is only possible for 90° increments.
* registering of turtle shapes. use a user-side made tilegrid is much easier.
* clone, turtles : there is no way to duplicate (deep copy) the turtle object, and no (easy) way to run 2 turtles on the same display 
* getturtle, getscreen : no use case.
* colormode : as we use a custom color object, and we don't set the colors manualy.


## French translation

First version for tests of translations. Use ~1KB more memory than english turtle. <br />
Première version pour tester les traductions. Utilise environ 1Ko de mémoire en plus par rapport a la tortue originale.<br/>
Documentation détaillée à venir.

### Usage

```python
from marius_turtle_french import Colors, turtle_fr

tortue = turtle_fr(display)
# pour utiliser moins de mémoire, appeler la tortue avec l'argument echelle:
# tortue = turtle_fr(display, echelle=2)


tortue.vitesse(6)
tortue.baissecrayon()

tortue.avance(60)
tortue.droite(90)
tortue.avance(60)
tortue.fixecap(tortue.vers(0,0))
tortue.aller(0,0)
tortue.fixecap(0)
```


### Liste des couleurs en français
NOIR, BLANC, ROUGE, JAUNE, VERT, ORANGE, BLEU, VIOLET, ROSE, GRIS, GRIS_CLAIR, BRUN, VERT_FONCE, TURQUOISE, BLEU_FONCE, ROUGE_FONCE<br />

### Liste des commandes en francais
* av, avance -> forward
* re, recule -> backward
* td, droite -> right
* tg, gauche -> left
* fixexy, aller, fpos, fixeposition -> goto
* degres -> degrees
* lc, levecrayon -> penup
* bc, baissecrayon -> pendown
* etatcrayon -> isdown
* origine -> home
* vitesse -> speed
* cercle -> circle
* cap -> heading
* fcap, fixecap -> setheading
* tc, tailleducrayon -> pensize
* cf, couleurfond -> bgcolor
* fce, fixecouleurecran -> bgcolor
* cc, couleurcrayon -> pencolor
* fcc, fixecouleurcrayon -> pencolor
* fif, fixeimagefond -> set_bgpic
* sif, supprimeimagefond -> del_bgpic
* montretortue -> showturtle
* cachetortue -> hideturtle
* estvisible -> isvisible
* changetortue -> changeturtle
* coordx -> xcor
* coordy -> ycor
* fixex -> setx
* fixey -> sety
* nettoie -> clear
* vers, directionde -> towards
* hauteurfenetre -> window_height
* largeurfenetre -> window_width
* point -> dot
* tamponne -> stamp
* detamponne -> clearstamp
* detamponnetout -> clearstamps
* reinitialise, reinit -> reset

