import thorpy
import parameters

class HUD:

    def __init__(self):
        self.life = thorpy.hud.HeartLife()
        self.bullets = thorpy.LifeBar.make("Bullets")
        self.bullets.stick_to("screen", "right", "right")
        self.bullets.set_topleft((None,5))
        self.score = thorpy.make_text("Score:   ",30,(255,0,0))
        self.score.stick_to("screen","bottom","bottom")

    def refresh_and_draw(self):
        hero = parameters.game.hero
        self.score.set_text("Score: "+str(parameters.game.score))
        self.life.blit(thorpy.get_screen(), hero.life/hero.max_life)
        self.bullets.set_life(hero.bullets/hero.max_bullets)
        self.bullets.blit()
        self.score.blit()