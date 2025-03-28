import pygame, sys
from .functions import INITIAL_WINDOW_SIZE

class Window:
    def __init__(self):
        self.fps = 60
        self.time = 1
        self.clock = pygame.time.Clock()
        self.display_scale = 1
        self.window_size = INITIAL_WINDOW_SIZE
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE | pygame.SCALED)
        self.display_surface = pygame.Surface((self.window_size[0]//self.display_scale, self.window_size[1]//self.display_scale))
    
    def update(self):
        self.clock.tick()
        self.calculate_dt()

        # print(self.clock.get_fps(), end='\r')
    
    def calculate_dt(self):
        # dt calculation
        try:
            self.dt = (1/self.clock.get_fps()) * self.time
        except:
            self.dt = 0