import pygame
from .top_down_entity import TopDownEntity

class Chess_Piece(TopDownEntity):
    def __init__(self, game, tile, color, chess_piece_type):
        super().__init__(game, tile, f'{color}_{chess_piece_type}', 'idle')
        self.color = color
        self.chess_piece_type = chess_piece_type

        self.load_collision_box_and_hit_box(chess_piece_type)

    def draw(self, surface, scroll=[0,0]):
        super().render_shadow(surface, scroll)
        super().draw(surface, scroll)
        pygame.draw.rect(surface, (255,0,0), [self.hit_box[0]-scroll[0], self.hit_box[1]-scroll[1], self.hit_box[2], self.hit_box[3]], 1)

