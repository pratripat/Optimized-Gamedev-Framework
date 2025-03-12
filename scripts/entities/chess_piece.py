from ..entity import Entity

class Chess_Piece(Entity):
    def __init__(self, game, tile, color, chess_piece_type):
        position = list(tile.keys())[0]
        super().__init__(f'{color}_{chess_piece_type}', position, game.animation_handler, 'idle')
        self.tile = tile
        self.game = game
        self.color = color
        self.chess_piece_type = chess_piece_type

    def update(self, dt):
        super().update(dt)

        self.move([], dt)
