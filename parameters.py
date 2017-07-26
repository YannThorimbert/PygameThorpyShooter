from pygame.math import Vector2 as V2

W,H = 400,600
BACKGROUND_TEXTURE = "sand-texture.jpg"

#vessel colors are defined in ship.py

ENGINE_FORCE = 0.8
ENGINE_FORCE_IA = 0.1
DRAG = 0.1
IA_LIFE = 0.5

BULLET_SPEED = 12
BULLET_SIZE = 7
BULLET_COLOR = (255,200,0)
MOD_BULLET = 4

MAX_BULLET_NUMBER = 100 #max number of bullets on screen
BULLET_SIZE_ON_2 = V2(BULLET_SIZE, BULLET_SIZE)/2

NSMOKE = 1 #1 = deactivate
IMMORTAL = True

game = None
