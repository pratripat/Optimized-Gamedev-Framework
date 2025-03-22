import pygame, sys, os
from .level import Level
from .window import Window
from .camera import Camera
from .renderer import Renderer
from .input_system import Input
from .animation_handler import Animation_Handler
from .entity_handler import Entity_Handler

pygame.init()

class Game:
    def __init__(self):
        self.time = 1
        
        self.window = Window()
        self.camera = Camera(self)
        self.renderer = Renderer(self)
        self.input = Input()
        self.animation_handler = Animation_Handler()

        # level stuff
        self.level = Level(self)
        self.level.load_level(0)

        # pawns gambit stuff
        self.player_color = 'black'
        self.enemy_color = 'white'

        # entity handler
        self.entity_handler = Entity_Handler(self)
        self.entity_handler.load_entities()

        # default camera settings
        self.camera.set_target(self.entity_handler.player)
        self.camera.set_speed(0.03)

        self.level.update_visible_tiles()

        self.current_game_state = [] # currently nthg is going on in the game

    def update(self):
        self.current_game_state.clear() # resetting the current game status to nthg

        self.window.update()        
        self.input.update()
        self.camera.update()
        self.level.update()
        self.renderer.update()
        # entity update
        self.entity_handler.update(self.window.dt)

    def render(self):
        self.renderer.render()
    
    def run(self):
        while 1:
            self.update()
            self.render()
        
    def set_camera_speed(self, speed):
        self.camera.set_speed(speed)
    
    def set_camera_target(self, target):
        self.camera.set_target(target)

    def set_collidables(self, collidable_ids):
        self.entity_handler.collidable_entity_ids = collidable_ids
        self.entity_handler.update_collidables()
    