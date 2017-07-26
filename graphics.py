import random
import thorpy
import ship
from parameters import *

bullet_img = None
smoke_gen = None
fire_gen = None
debris_hero = None
all_debris = None
all_explosions = []
explosions = [[],[],[]]
expl_sizes = [(60,60), (80,80), (120,120)]
current_explosion = [0,0,0]


def generate_debris_explosion(pos, generator):
    angle = random.randint(0,360) #pick random angle
    spread = 180 #spread of debris directions
    generator.generate(pos, #position
                        n=100, #number of debris
                        v_range=(10,50), #translational velocity range
                        omega_range=(5,25), #rotational velocity range
                        angle_range=(angle-spread,angle+spread))

def generate_debris_hit(pos, vel, generator):
    angle = int(vel.angle_to(V2(0,1)))
    spread = 10 #spread of debris directions
    generator.generate( pos, #position
                        n=1, #number of debris
                        v_range=(20,50), #translational velocity range
                        omega_range=(5,25), #rotational velocity range
                        angle_range=(angle-spread,angle+spread))


def initialize():
    global bullet_img, smoke_gen, fire_gen, debris_hero, all_debris
    bullet_img = thorpy.graphics.get_aa_ellipsis((BULLET_SIZE,BULLET_SIZE),
                                                    BULLET_COLOR)
    bullet_img = thorpy.graphics.get_shadow(bullet_img, color=(255,155,0))
    smoke_gen = thorpy.fx.get_smokegen(n=NSMOKE, color=(20,20,20), grow=0.6)
    fire_gen = thorpy.fx.get_fire_smokegen(n=NSMOKE, color=(200,255,155),
                                            grow=0.4, size0=(7,7))
    debris_hero = thorpy.fx.get_debris_generator(duration=50,
                                                     color=ship.Hero.color,
                                                     max_size=8)
    ship.EnnemySimple.debris = thorpy.fx.get_debris_generator(duration=50,
                                                color=ship.EnnemySimple.color,
                                                max_size=8)
    ship.EnnemyFollower.debris = thorpy.fx.get_debris_generator(duration=50,
                                                color=ship.EnnemyFollower.color,
                                                max_size=8)
    all_debris = [debris_hero, ship.EnnemySimple.debris, ship.EnnemyFollower.debris]
    print(ship.EnnemySimple.debris, ship.EnnemyFollower.debris)
    for size in range(3):
        for i in range(10):
            e = thorpy.AnimatedGif.make(random.choice(["explosion-illugion.gif",
                                                        "explosion.gif"]))
            e.resize_frames(expl_sizes[size])
            e.set_visible(False)
            e.nread = 8
            e.low = 6
            explosions[size].append(e)
            all_explosions.append(e)

def add_explosion(ship):
    M = max(ship.size)
    if M < 20:
        size = 0
    elif M < 30:
        size = 1
    else:
        size = 2
    expl = explosions[size][current_explosion[size]]
    expl.set_visible(True)
    expl.nread = 1
    expl.set_center(ship.element.get_fus_center())
##    expl.move((0,-expl_sizes[size][1]//3))
    current_explosion[size] += 1
    current_explosion[size] %= len(explosions[size])



