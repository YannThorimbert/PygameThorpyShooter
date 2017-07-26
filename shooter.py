import pygame, math, random
from pygame.math import Vector2 as V2
import thorpy

from ship import Hero
import parameters as p
from gamelogic import *
from graphics import debris_hero, fire_gen, smoke_gen, bullet_img
import graphics


# ##############################################################################

app = thorpy.Application((W,H), "ThorPy shooter example")

graphics.initialize()


e_background = thorpy.Background.make(image=p.BACKGROUND_TEXTURE,
                                        elements=graphics.all_explosions)
##e_background = thorpy.Background.make((255,255,255))
hero = Hero(size=(20,20), life=100, pos=(p.W//2,p.H-100), bullets=3000)
game = Game(e_background, hero)

p.game = game
commands = thorpy.commands.Commands(e_background,-1)
commands.refresh = game.refresh

screen = thorpy.get_screen()
menu = thorpy.Menu(e_background, fps=45)
##thorpy.application.SHOW_FPS = True
pygame.key.set_repeat(30,30)
menu.play()
app.quit()

