import pygame
from .entities.player import Player
from .entities.enemy import Enemy

class Entity_Handler:
    def __init__(self, game):
        self.game = game
    
    def load_entities(self):
        player_tile = self.game.level.tilemap.get_tiles_with_id('player')
        self.player = Player(self.game, player_tile)

        # self.player.velocity = pygame.Vector2(0.2, 0)

        enemy_tiles = self.game.level.tilemap.get_tiles_with_id('enemies')
        self.enemies = []
        for tile_pos in enemy_tiles:
            enemy = Enemy(self.game, {tile_pos: enemy_tiles[tile_pos]})
            self.enemies.append(enemy)

        self.entity_group = pygame.sprite.Group()
        self.entity_group.add(self.player, *self.enemies)
    
    def update(self, dt):
        self.entity_group.update(dt)
    
    def draw(self, surface):
        # self.entity_group.draw(surface)
        for entity in self.entity_group:
            entity.draw(surface, scroll=self.game.camera.scroll)