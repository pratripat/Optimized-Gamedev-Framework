import pygame
from ..entity import Entity

class TopDownEntity(Entity):
    def __init__(self, game, tile, animation_id, default_animation, speed=1, max_health=100):
        position = list(tile.keys())[0]
        super().__init__(animation_id, position, game.animation_handler, default_animation)
        self.game = game
        self.tile = tile

        self.speed  = speed
        self.health = max_health

    def load_collision_box_and_hit_box(self, id=None):
        if id == None: id = self.id

        from ..functions import COLLISION_BOXES
        collision_box = COLLISION_BOXES[id]['collision_box']
        hit_box = COLLISION_BOXES[id]['hit_box']

        self.hit_box_data = [hit_box[0]*self.scale, hit_box[1]*self.scale, hit_box[2]*self.scale, hit_box[3]*self.scale]

        collision_box = pygame.FRect(collision_box[0]*self.scale, collision_box[1]*self.scale, collision_box[2]*self.scale, collision_box[3]*self.scale)
        self.set_rect(collision_box)

    def update(self, collidable_rects, dt):
        super().update(dt)

        self.update_state()
        self.update_animation()
        self.move(collidable_rects, dt)
    
    def update_state(self):
        self.state = {'idle': False, 'moving': False, 'shooting': False, 'special_attack': False}

        if self.velocity.x != 0 or self.velocity.y != 0:
            self.state['moving'] = True
        else:
            self.state['idle'] = True
        
    def update_animation(self, states_to_animation={'idle': 'idle', 'moving': 'moving'}):
        animation_state = states_to_animation['idle']
        
        if self.state['moving']: 
            animation_state = states_to_animation['moving']

        self.set_animation(animation_state)
    
    @property
    def hit_box(self):
        return pygame.FRect(self.rect.x-self.offset.x+self.hit_box_data[0], self.rect.y-self.offset.y+self.hit_box_data[1], self.hit_box_data[2], self.hit_box_data[3])

    @property
    def dead(self):
        return self.health <= 0

class TopDownPlayer(TopDownEntity):
    def __init__(self, game, tile, animation_id, default_animation='idle'):
        super().__init__(game, tile, animation_id, default_animation)
    
    def update(self, collidable_rects, dt):
        self.update_inputs()

        super().update(collidable_rects, dt)

        self.handle_directions()

    def update_inputs(self):
        self.directions = {'top': False, 'right': False, 'bottom': False, 'left': False}

        if any(key in self.game.input.keys_held for key in [pygame.K_w, pygame.K_UP]):
            self.directions['top'] = True
        if any(key in self.game.input.keys_held for key in [pygame.K_d, pygame.K_RIGHT]):
            self.directions['right'] = True
        if any(key in self.game.input.keys_held for key in [pygame.K_s, pygame.K_DOWN]):
            self.directions['bottom'] = True
        if any(key in self.game.input.keys_held for key in [pygame.K_a, pygame.K_LEFT]):
            self.directions['left'] = True
    
    def handle_directions(self):
        key_left = self.speed * int(self.directions['left'])
        key_right = self.speed * int(self.directions['right'])
        key_top = self.speed * int(self.directions['top'])
        key_bottom = self.speed * int(self.directions['bottom'])

        self.velocity.x = key_right - key_left
        self.velocity.y = key_bottom - key_top

        # Diagonal speed
        if self.velocity.x != 0 and self.velocity.y != 0:
            #basically multiplying the velocity with 1/(root of 2).
            self.velocity *= 0.707107