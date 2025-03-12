from ..entity import Entity

class Chess_Piece(Entity):
    def __init__(self, game, tile, color, chess_piece_type):
        position = list(tile.keys())[0]
        super().__init__(f'{color}_{chess_piece_type}', position, game.animation_handler, 'idle')
        self.tile = tile
        self.game = game
        self.color = color
        self.chess_piece_type = chess_piece_type
        self.speed = 1 # default speed

    def update(self, dt):
        super().update(dt)

        self.update_state()
        self.update_animation()
        self.move([], dt)
    
    def update_state(self):
        self.state = {'idle': False, 'moving': False, 'shooting': False, 'special_attack': False}

        if self.velocity.x != 0 or self.velocity.y != 0:
            self.state['moving'] = True
        else:
            self.state['idle'] = True
    
    def update_animation(self):
        animation_state = 'idle'
        
        if self.state['moving']:
            animation_state = 'moving'

        self.set_animation(animation_state)
