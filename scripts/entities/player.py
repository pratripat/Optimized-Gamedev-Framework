import pygame
from .chess_piece import Chess_Piece

class Player(Chess_Piece):
    def __init__(self, game, tile):
        super().__init__(game, tile, game.player_color, 'pawn')
        self.speed = 2

    def update(self, dt):
        self.update_inputs()

        super().update(dt)

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

        # if not self.special_attack and self.game.input.mouse_states['left_held']:
        #     self.shoot()

        # if self.special_attack and self.game.input.mouse_states['left']:
        #     self.perform_special_attack()

        # if any(key in self.game.input.keys_held for key in [pygame.K_LSHIFT, pygame.K_RSHIFT]):
        #     self.check_special_attack()
        # elif self.special_attack:
        #     self.reset_special_attack()

        # if self.can_swap and self.game.input.mouse_states['right']:
        #     self.swap_cards()
        #     self.game.cards_menu = True
    
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