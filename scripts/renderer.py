import pygame, math

class Renderer:
    def __init__(self, game):
        self.game = game
        self.layers_to_be_rendered = ['path', 'vegetation']

    def render(self):
        self.game.window.display_surface.fill((0, 0, 0))
        scroll = self.game.camera.scroll
        
        for layer_id, chunks in self.visible_tiles_data.items():
            for chunk_pos, tiles in chunks.items():
                for tile_pos, tile in tiles.items():
                    self.game.window.display_surface.blit(tile['image'], [tile_pos[0]-scroll.x, tile_pos[1]-scroll.y])

        self.game.entity_handler.draw(self.game.window.display_surface)

        pygame.draw.rect(self.game.window.display_surface, 'white', (-self.game.camera.scroll[0], -self.game.camera.scroll[1], 32*8*3, 32*8*3), 1)

        self.game.window.screen.blit(pygame.transform.scale(self.game.window.display_surface, self.game.window.window_size), (0, 0))

        pygame.display.update()
    
    def update_visible_tiles(self):
        self.visible_tiles_data = self.game.level.tilemap.get_visible_tiles(pygame.Rect(*self.game.camera.scroll, 1200, 600), self.layers_to_be_rendered)
