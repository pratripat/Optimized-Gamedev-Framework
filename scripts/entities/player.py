from .top_down_entity import TopDownPlayer

class Player(TopDownPlayer):
    def __init__(self, game, tile):
        super().__init__(game, tile, 'black_pawn')
        self.speed = 2

        self.load_collision_box_and_hit_box('pawn')
    
