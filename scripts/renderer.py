import pygame, math

class Renderer:
    def __init__(self, game):
        self.game = game

    def render(self):
        self.game.window.display_surface.fill((0, 0, 0))
        
        self.game.level.render()

        # self.game.window.screen.blit(pygame.transform.scale(self.game.window.display_surface, self.game.window.window_size), (0, 0))

        self.game.window.screen.blit(self.game.window.display_surface, (0, 0))

        pygame.display.update()
