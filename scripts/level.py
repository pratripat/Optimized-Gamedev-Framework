import pygame
from .tilemap import Tilemap

class Level:
    def __init__(self, game):
        self.game = game
        self.layers_to_be_rendered = ['path']
    
    def load_level(self, level):
        self.levels = ['chumma']
        
        self.tilemap = Tilemap(f'data/levels/{self.levels[0]}.json', layer_ids_for_chunk_images=self.layers_to_be_rendered)
    
    def render(self):
        scroll = self.game.camera.scroll

        # for _, chunks in self.visible_tiles_data.items():
        #     for _, tiles in chunks.items():
        #         for tile_pos, tile in tiles.items():
        #             self.game.window.display_surface.blit(tile['image'], [tile_pos[0]-scroll.x, tile_pos[1]-scroll.y])

        self.tilemap.render(self.game.window.display_surface, scroll, self.visible_tiles_data, self.layers_to_be_rendered)

        self.game.entity_handler.draw(self.game.window.display_surface)

        # debug
        pygame.draw.rect(self.game.window.display_surface, 'white', (-self.game.camera.scroll[0], -self.game.camera.scroll[1], 32*8*3, 32*8*3), 1)
    
    def update(self):
        if 'cameramovement' in self.game.current_game_state:
            self.update_visible_tiles()
    
    def update_visible_tiles(self):
        self.visible_tiles_data = self.game.level.tilemap.get_visible_tiles(pygame.Rect(*self.game.camera.scroll, *self.game.window.window_size), self.layers_to_be_rendered)

    def is_visible(self, rect):
        return pygame.Rect(*self.game.camera.scroll, *self.game.window.window_size).colliderect(rect)