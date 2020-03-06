# FRENCH TRANSLATION FOR adafruit_turtle
#from adafruit_turtle import turtle
from marius_turtle import turtle


class Couleur(object):
    """Couleurs standart"""
    BLANC = 0xFFFFFF
    NOIR = 0x000000
    ROUGE = 0xFF0000
    ORANGE = 0xFFA500
    JAUNE = 0xFFEE00
    VERT = 0x00C000
    BLEU = 0x0000FF
    VIOLET = 0x8040C0
    ROSE = 0xFF40C0
    GRIS_CLAIR = 0xAAAAAA
    GRIS = 0x444444
    BRUN = 0xCA801D
    VERT_FONCE = 0x008700
    TURQUOISE = 0x00C0C0
    BLEU_FONCE = 0x0000AA
    ROUGE_FONCE = 0x800000

    couleurs = (NOIR, BLANC, ROUGE, JAUNE, VERT, ORANGE, BLEU, VIOLET, ROSE,
                GRIS, GRIS_CLAIR, BRUN, VERT_FONCE, TURQUOISE, BLEU_FONCE, ROUGE_FONCE)
    colors = couleurs

    def __init__(self):
        pass

Color = Couleur

class turtle_fr(turtle):
    """Une Tortue a laquelle on donne des commandes pour dessiner"""

    def __init__(self, display=None, scale=1):
        super().__init__(display, scale)
        #print("Tortue en francais en attente des ordres.")
        self.av = self.avance = self.forward
        self.degres = self.degrees

        self.re = self.recule = self.backward
        self.td = self.droite = self.right
        self.tg = self.gauche = self.left
        self.fixexy = self.aller = self.goto
        self.fpos = self.fixeposition = self.goto

        self.lc = self.levecrayon = self.penup
        self.bc = self.baissecrayon = self.pendown
        self.etatcrayon = self.isdown

        self.origine = self.home
        self.vitesse = self.speed
        self.cercle = self.circle

        self.cap = self.heading
        self.fcap = self.fixecap = self.setheading

        self.tc = self.tailleducrayon = self.pensize
        self.cf = self.couleurfond = self.bgcolor
        self.fcf = self.fixecouleurfond = self.bgcolor

        self.cc = self.couleurcrayon = self.pencolor
        self.fcc = self.fixecouleurcrayon = self.pencolor

        self.imagefond = self.bgpic

        self.montretortue = self.showturtle
        self.cachetortue = self.hideturtle
        self.estvisible = self.isvisible
        self.changetortue = self.changeturtle

        self.coordx = self.xcor
        self.coordy = self.ycor

        self.fixex = self.setx
        self.fixey = self.sety

        self.nettoie = self.clear
        self.vers = self.directionde = self.towards

        self.hauteurfenetre = self.window_height
        self.largeurfenetre = self.window_width
        self.point = self.dot
        self.tamponne = self.stamp
        self.detamponne = self.clearstamp
        self.detamponnetout = self.clearstamps
        self.reinitialise = self.reinit = self.reset







