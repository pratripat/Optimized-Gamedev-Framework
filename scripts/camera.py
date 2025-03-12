import pygame, random

class Camera:
    def __init__(self, game, target=None):
        self.game = game
        self.target = target
        self.scroll = pygame.math.Vector2(0,0)
        self.time = 0
        self.speed = 1
        self.screen_shake = 0

    def update(self, constraints=None):
        if self.time == 0:
            self.screen_shake = 0

        #Moves camera towards target
        if self.target:
            delx = (self.target.center[0]-self.scroll.x-self.game.window.display_surface.get_width()/2) * self.speed + random.uniform(-self.screen_shake, self.screen_shake)
            dely = (self.target.animation_center[1]-self.scroll.y-self.game.window.display_surface.get_height()/2) * self.speed + random.uniform(-self.screen_shake, self.screen_shake)
            self.scroll.x += delx
            self.scroll.y += dely

            if (abs(delx) > self.screen_shake or abs(dely) > self.screen_shake):
                self.game.renderer.update_visible_tiles()

        if self.time > 0:
            self.time -= 1

        #Keeps camera within the constraints rect
        if constraints:
            if self.scroll[1] < constraints.top:
                self.scroll[1] = constraints.top
            if self.scroll[1] > constraints.bottom-self.game.window.display_surface.get_height()+self.game.tilemap.TILE_RES:
                self.scroll[1] = constraints.bottom-self.game.window.display_surface.get_height()+self.game.tilemap.TILE_RES
            if self.scroll[0] < constraints.left:
                self.scroll[0] = constraints.left
            if self.scroll[0] > constraints.right-self.game.window.display_surface.get_width()+self.game.tilemap.TILE_RES:
                self.scroll[0] = constraints.right-self.game.window.display_surface.get_width()+self.game.tilemap.TILE_RES

    def set_target(self, target):
        self.target = target

    def set_speed(self, speed):
        self.speed = speed

    def set_screen_shake(self, screen_shake, time):
        self.screen_shake = screen_shake
        self.time = time