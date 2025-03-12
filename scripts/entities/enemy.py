from .chess_piece import Chess_Piece

class Enemy(Chess_Piece):
    def __init__(self, game, tile):
        super().__init__(game, tile, game.enemy_color, 'knight')