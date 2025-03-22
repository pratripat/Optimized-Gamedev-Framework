import pygame
from .tilemap import Tilemap

class Level:
    def __init__(self, game):
        self.game = game
        self.layers_to_be_rendered = ['path']
    
    def load_level(self, level):
        self.levels = ['trial']
        
        self.tilemap = Tilemap(f'data/levels/{self.levels[0]}.json', layer_ids_for_chunk_images=self.layers_to_be_rendered)
    
    def render_tilemap(self):
        scroll = self.game.camera.scroll

        self.tilemap.render(self.game.window.display_surface, scroll, self.visible_tiles_data, self.layers_to_be_rendered)
        
        pygame.draw.rect(self.game.window.display_surface, (255,0,0), [-self.game.camera.scroll[0], -self.game.camera.scroll[1], self.tilemap.CHUNK_SIZE*self.tilemap.TILE_RES, self.tilemap.CHUNK_SIZE*self.tilemap.TILE_RES], 1)
            
    def update(self):
        if 'cameramovement' in self.game.current_game_state:
            self.update_visible_tiles()
    
    def update_visible_tiles(self):
        self.visible_tiles_data = self.tilemap.get_visible_tiles(pygame.Rect(*self.game.camera.scroll, *self.game.window.window_size), self.layers_to_be_rendered)

    def is_visible(self, rect):
        return pygame.Rect(*self.game.camera.scroll, *self.game.window.window_size).colliderect(rect)