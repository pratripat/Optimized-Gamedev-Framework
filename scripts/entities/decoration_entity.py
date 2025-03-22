import pygame
from ..functions import COLLISION_BOXES, SCALE

class DecorationEntity(pygame.sprite.Sprite):
    def __init__(self, game, id, decoration_id, position, chunk_pos, spritesheet_index):
        super().__init__()
        self.game = game
        self.id = id
        self.decoration_id = decoration_id
        self.chunk_pos = chunk_pos
        self.spritesheet_index = spritesheet_index
        self.animation_id = f'vegetation_{spritesheet_index}'
        self.animation = game.animation_handler.get_animation(self.animation_id)
        
        self.flipped = False

        self.load_rect(position)
    
    def load_rect(self, position):
        self.collision_box = COLLISION_BOXES[self.decoration_id][str(self.spritesheet_index)]

        self.rect = pygame.FRect(position[0], position[1], self.collision_box[2]*SCALE, self.collision_box[3]*SCALE)
        self.offset = pygame.math.Vector2(self.collision_box[0]*SCALE, self.collision_box[1]*SCALE)

        self.rect.topleft += self.offset

    def draw(self, surface, scroll=[0,0], colorkey=None, vertical_flip=False, angle=0, position=None, visible_rect=None, alpha=None, animation_offset=None):
        if not position: position = self.position
        self.animation.render(surface, (position[0]-scroll.x, position[1]-scroll.y), [self.flipped, vertical_flip], colorkey, angle=angle, alpha=alpha, animation_offset=animation_offset)

        pygame.draw.rect(surface, (255,0,0), [self.rect[0]-scroll.x, self.rect[1]-scroll.y, self.rect[2], self.rect[3]], 1)

    def update(self, dt):
        self.animation.run(dt)

    @property
    def position(self):
        return self.rect.topleft - self.offset

    @property
    def animation_center(self):
        return [self.position[0]+self.image.get_width()/2, self.position[1]+self.image.get_height()/2]

    @property
    def image(self):
        return self.animation.image