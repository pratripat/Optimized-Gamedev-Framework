import pygame, random

class Camera:
    def __init__(self, game, target=None):
        self.game = game
        self.target = target
        self.scroll = pygame.math.Vector2(0,0)
        self.time = 0
        self.speed = 1
        self.screen_shake = 0
        
        self.follow_cursor = False
        self.cursor_following_ratio = 0.05

    def follow_cursor(self, cursor_following_ratio=0.05):
        self.follow_cursor = True
        self.cursor_following_ratio = cursor_following_ratio

    def update(self, constraints=None):
        if self.time == 0:
            self.screen_shake = 0

        #Moves camera towards target
        if self.target:
            position = self.target.animation_center
            
            if self.follow_cursor: 
                cursor = self.game.input.mouse_position
                position[0] += (cursor[0] - position[0] + self.scroll.x) * self.cursor_following_ratio
                position[1] += (cursor[1] - position[1] + self.scroll.y) * self.cursor_following_ratio

            delx = round((position[0]-self.scroll.x-self.game.window.display_surface.get_width()/2) * self.speed + random.uniform(-self.screen_shake, self.screen_shake), 2)
            dely = round((position[1]-self.scroll.y-self.game.window.display_surface.get_height()/2) * self.speed + random.uniform(-self.screen_shake, self.screen_shake), 2)
            self.scroll.x += delx
            self.scroll.y += dely

            # updating game state
            if (abs(delx) > 0 or abs(dely) > 0):
                self.game.current_game_state.append('cameramovement')

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