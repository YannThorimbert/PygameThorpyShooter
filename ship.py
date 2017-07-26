import random
import pygame
from pygame.math import Vector2 as V2
import thorpy
import parameters as p
import graphics
from bullet import Bullet

class Ship:
    id = 0
    debris = None

    def __init__(self, size, life, pos, bullets=100):
        self.size = size
        self.life = life
        self.max_life = life
        self.pos = V2(pos)
        self.vel = V2()
        self.bullets = bullets
        self.max_bullets = bullets
        self.can_explode = True
        self.id = Ship.id
        Ship.id += 1
        self.element = thorpy.Image.make(color=self.color)
        self.element.set_size(self.size)
        if thorpy.constants.CAN_SHADOWS: #set shadow
            thorpy.makeup.add_static_shadow(self.element,
                                            {"target_altitude":5,
                                                "shadow_radius":3,
                                                "sun_angle":40,
                                                "alpha_factor":0.6})
        self.smoking = False

    def refresh(self):
        self.vel -= p.DRAG*self.vel #natural braking due to drag
        if self.pos.x > p.W and self.vel.x > 0: #bounce on the right
            self.vel *= -1
        elif self.pos.x < 0 and self.vel.x < 0: #bounce on the left
            self.vel *= -1
        self.move(self.vel)
        for bullet in p.game.bullets:
            if bullet.from_id != self.id:
                if bullet.visible:
    ##                if self.element.get_rect().collidepoint(bullet.pos):
                    r = self.element.get_rect()
                    if bullet.pos.distance_to(r.center) < r.w:
                        bullet.visible = False
                        self.life -= 1
                        if self.debris:
                            print("Gen", type(self))
                            graphics.generate_debris_hit(V2(bullet.pos+(0,-10)),
                                                V2(bullet.v),
                                                self.debris)
                        if self.life < self.max_life/2.:
                            self.smoking = True
                        else:
                            self.smoking = False
        if self.life <= 0:
            if self.debris:
                graphics.generate_debris_explosion(V2(self.element.get_fus_center()), self.debris)
            if self.can_explode:
                expl = graphics.add_explosion(self)
            p.game.ships.remove(self)
            p.game.e_background.remove_elements([self.element])
            if self is p.game.hero:
                p.game.hero_dead.activate()
            else:
                p.game.score += 1 #faire avec un GameEvent !!!
        elif self.smoking:
            graphics.smoke_gen.generate(self.element.get_rect().midtop)

    def move(self, delta):
        self.pos += delta
        self.element.set_center(self.pos)

    def shoot(self, vel):
        if self.bullets > 0:
            if len(p.game.bullets) > p.MAX_BULLET_NUMBER:
                p.game.bullets.popleft()
            v = V2(vel)
            p.game.bullets.append(Bullet(V2(self.pos)-p.BULLET_SIZE_ON_2, v, self.id))
            self.bullets -= 1

class EnnemySimple(Ship):
    color = (255,0,0)

    def __init__(self, pos):
        size = (random.randint(10,50),)*2
        life = 2*size[0]*p.IA_LIFE
        bullets = life
        Ship.__init__(self, size, life, pos, bullets)


    def ia(self):
        if self.element.get_rect().colliderect(p.game.hero.element.get_rect()):
            if not p.IMMORTAL:
                p.game.hero.life = -1
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA

class EnnemyFollower(Ship):
    color = (255,255,0)

    def __init__(self, pos):
        size = (random.randint(10,50),)*2
        life = 2*size[0]*p.IA_LIFE
        bullets = life
        Ship.__init__(self, size, life, pos, bullets)

    def ia(self):
        if self.element.get_rect().colliderect(p.game.hero.element.get_rect()):
            p.game.hero.life = -1
            self.life = -1
        elif self.pos.y < 3*p.H//4:
            d = p.game.hero.pos - self.pos
            self.vel += d.normalize()*p.ENGINE_FORCE_IA
            if random.random() < 0.1:
                self.shoot(self.vel.normalize()*p.BULLET_SPEED)
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA
        graphics.fire_gen.generate(self.pos)


class LifeStock(Ship):
    color = (255,255,255)

    def __init__(self, pos):
        life = 100
        size = (random.randint(1,5)*10,)*2
        Ship.__init__(self, size, life, pos, 0)
        self.can_explode = False


    def ia(self):
        if self.element.get_rect().colliderect(p.game.hero.element.get_rect()):
            p.game.hero.life += self.element.get_rect().w
            p.game.hero.life = min(p.game.hero.life, 100)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA*2

class BulletStock(Ship):
    color = (0,0,0)

    def __init__(self, pos):
        life = 100
        size = (random.randint(1,5)*10,)*2
        Ship.__init__(self, size, life, pos, 0)
        self.can_explode = False


    def ia(self):
        if self.element.get_rect().colliderect(p.game.hero.element.get_rect()):
            p.game.hero.bullets += self.element.get_rect().w*2
            p.game.hero.bullets = min(p.game.hero.max_bullets, p.game.hero.bullets)
            self.life = -1
        else:
            self.vel += V2(0,1)*p.ENGINE_FORCE_IA*2

class Hero(Ship):
    color = (0,0,255)

    def ia(self):
        # process key pressed
        pp = pygame.key.get_pressed()
        if pp[pygame.K_LEFT]:
            self.vel[0] -= p.ENGINE_FORCE
        elif pp[pygame.K_RIGHT]:
            self.vel[0] += p.ENGINE_FORCE
        if pp[pygame.K_SPACE]:
            if p.game.i%p.MOD_BULLET == 0:
                self.shoot((0,-p.BULLET_SPEED))

coming = [EnnemySimple,EnnemyFollower,]*3+ [LifeStock, BulletStock]