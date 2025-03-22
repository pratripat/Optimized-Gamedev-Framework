import pygame, math, random
from .vfx.vfx_manager import VFX

class Renderer:
    def __init__(self, game):
        self.game = game
        self.vfx_manager = VFX(game)
        self.vfx_manager.particle_system.add_particles(100, [480, 230], [random.uniform(-1,1),1], decay_rate=0.01)

    def render(self):
        # clearing the surface
        self.game.window.display_surface.fill((0, 0, 0))

        # renderingthe whole level
        self.game.level.render_tilemap()
        
        self.vfx_manager.render(self.game.window.display_surface, self.game.camera.scroll)

        # rendering the entities
        self.game.entity_handler.draw(self.game.window.display_surface)

        # only if the whole display surface is to be rendered according to some scale
        # self.game.window.screen.blit(pygame.transform.scale(self.game.window.display_surface, self.game.window.window_size), (0, 0))

        # this is just if the scale is 1 
        self.game.window.screen.blit(self.game.window.display_surface, (0, 0))

        # updating the display
        pygame.display.update()

    def update(self):
        self.vfx_manager.update(self.game.window.dt)
