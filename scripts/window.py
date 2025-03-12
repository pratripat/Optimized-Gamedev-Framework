import pygame, sys

class Window:
    def __init__(self):
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.display_scale = 1
        self.window_size = (1200, 600)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE | pygame.SCALED)
        self.display_surface = pygame.Surface((self.window_size[0]//self.display_scale, self.window_size[1]//self.display_scale))
    
    def update(self):
        self.clock.tick()
        self.calculate_dt()
    
    def calculate_dt(self):
        # dt calculation
        try:
            self.dt = 1/self.clock.get_fps()
        except:
            self.dt = 0