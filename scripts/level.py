from .tilemap import Tilemap

class Level:
    def __init__(self, game):
        self.game = game
    
    def load_level(self, level):
        self.levels = ['trial']
        
        self.tilemap = Tilemap(f'data/levels/{self.levels[0]}.json')
