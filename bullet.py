from pygame.math import Vector2 as V2
import thorpy
import graphics

class Bullet:

    def __init__(self, pos, v, from_id):
        self.pos = pos
        self.v = V2(v)
        self.from_id = from_id
        self.visible = True

    def refresh(self):
        self.pos += self.v

    def draw(self):
        if self.visible:
            thorpy.get_screen().blit(graphics.bullet_img, self.pos)