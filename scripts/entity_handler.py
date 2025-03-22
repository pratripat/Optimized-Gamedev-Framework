import pygame
from .entities.player import Player
from .entities.enemy import Enemy
from .entities.decoration_entity import DecorationEntity

class Entity_Handler:
    def __init__(self, game):
        self.game = game

        # Initialization
        self.collidables_rects = []
        self.sorted_entities = []
        self.collidable_entity_ids = []
    
    def load_entities(self):
        # Loads the player
        player_tile = self.game.level.tilemap.get_tiles_with_id('player')
        self.player = Player(self.game, player_tile)

        # Loads the enemies 
        enemy_tiles = self.game.level.tilemap.get_tiles_with_id('enemies')
        self.enemies = []
        for tile_pos in enemy_tiles:
            enemy = Enemy(self.game, {tile_pos: enemy_tiles[tile_pos]})
            self.enemies.append(enemy)
            enemy.velocity.x = 1

        self.entity_group = pygame.sprite.Group()
        self.entity_group.add(self.player, *self.enemies)

        # Loads the vegetation
        vegetation_tiles = self.game.level.tilemap.get_tiles_with_id('vegetation')
        self.vegetation = []
        for tile_pos in vegetation_tiles:
            vegetation = DecorationEntity(self.game, vegetation_tiles[tile_pos]['id'], 'vegetation', tile_pos, vegetation_tiles[tile_pos]['chunk_position'], vegetation_tiles[tile_pos]['spritesheet_index'])
            self.vegetation.append(vegetation)
        
        self.vegetation_group = pygame.sprite.Group()
        self.vegetation_group.add(*self.vegetation)
    
    def update(self, dt):
        self.update_collidables()
        
        self.entity_group.update(self.collidables_rects, dt)
        self.vegetation_group.update(dt)

        if 'cameramovement' in self.game.current_game_state:
            self.sorted_entities = self.y_sort_entities()
    
    def draw(self, surface):
        # render in a particular order
        for entity in self.sorted_entities:
          entity.draw(surface, scroll=self.game.camera.scroll)

    def update_collidables(self):
        # Only if there has been a movement we update the collidables
        if 'cameramovement' not in self.game.current_game_state: return 

        self.collidables_rects.clear()
        chunks = []

        # Getting the chunks of the collidable entities
        for id in self.collidable_entity_ids:
            chunk, chunk_pos = self.game.level.tilemap.get_chunk(id, self.player.position)
            chunks = self.game.level.tilemap.get_neighbor_chunks(id, chunk_pos)
            chunks.append(chunk_pos)

        # Getting the collidable entities
        for entity in self.vegetation_group.sprites():
            if entity.chunk_pos not in chunks: continue
            self.collidables_rects.append(entity.rect)

    # sorts the entities based on their y position (center of the image)
    def y_sort_entities(self): 
        total_entities = self.entity_group.sprites() + self.vegetation_group.sprites()
        sorted_entities = sorted(total_entities, key=lambda entity: entity.rect[1])

        return sorted_entities