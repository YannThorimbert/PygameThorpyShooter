import random
from collections import deque
import pygame
from pygame.math import Vector2 as V2
import thorpy
from ship import coming
from hud import HUD
from parameters import W, H, ENGINE_FORCE, MOD_BULLET, BULLET_SPEED
import parameters as p
import graphics as g

import thorpy.gamestools.monitoring as monitoring

class GameEvent:

    def __init__(self, delay, reaction, game):
        self.delay = delay
        self.reaction = reaction
        self.i = float("inf")
        self.game = game

    def activate(self):
        self.i = p.game.i

    def refresh(self):
        if self.game.i - self.i >= self.delay:
            self.reaction()

mon = monitoring.Monitor()

class Game:

    def __init__(self, e_background, hero):
        self.e_background = e_background
        self.screen = thorpy.get_screen()
        self.ships = []
        self.bullets = deque()
        self.hero = hero
        self.add_ship(hero)
        self.i = 0
        self.hero_dead = GameEvent(50,thorpy.functions.quit_menu_func,self)
        self.events = [self.hero_dead]
        self.hud = HUD()
        self.score = 0

    def refresh(self):
        mon.append("a")
        for e in self.events:
            e.refresh()
        if self.i % 50 == 0:
            Coming = random.choice(coming)
            self.add_ship(Coming(pos=(random.randint(20,W-20),0)))
        # process key pressed
        pp = pygame.key.get_pressed()
        if pp[pygame.K_LEFT]:
            move_hero_left()
        elif pp[pygame.K_RIGHT]:
            move_hero_right()
        if pp[pygame.K_SPACE]:
            if self.i%MOD_BULLET == 0:
                self.hero.shoot((0,-BULLET_SPEED))
        for ship in self.ships:
            ship.ia()
            ship.refresh()
        mon.append("b")
        # refresh bullets
        for bullet in self.bullets:
            bullet.refresh()
        mon.append("c")
        # process smoke
        g.smoke_gen.kill_old_elements()
        g.fire_gen.kill_old_elements()
        mon.append("d")
        if p.NSMOKE > 1:
            g.smoke_gen.update_physics(V2())
            g.fire_gen.update_physics(V2())
        mon.append("e")
        # process debris
        for d in g.all_debris:
            d.kill_old_elements(self.screen.get_rect())
            d.update_physics(dt=0.1)
        mon.append("f")
        # refresh screen
        self.e_background.blit()
        mon.append("g")
        if p.NSMOKE > 1:
            g.smoke_gen.draw(self.screen)
            g.fire_gen.draw(self.screen)
        mon.append("h")
        for bullet in self.bullets:
            bullet.draw()
        mon.append("i")
        for d in g.all_debris:
            d.draw(self.screen)
        mon.append("j")
        self.hud.refresh_and_draw()
        pygame.display.flip()
        self.i += 1
        mon.append("k")

    def add_ship(self, ship):
        self.ships.append(ship)
        self.e_background.add_elements([ship.element])

    def showmon(self):
        mon.show()

def move_hero_left():
    p.game.hero.vel[0] -= ENGINE_FORCE
def move_hero_right():
    p.game.hero.vel[0] += ENGINE_FORCE

##a->b: 10.988798017052154
##b->c: 0.25446000916870104
##c->d: 56.777791985411895
##d->e: 0.04531470242082873
##e->f: 17.482862172074608
##f->g: 8.166405939950124
##g->h: 4.8219657055277985