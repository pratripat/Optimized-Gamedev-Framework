import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, id, position, animation_handler, current_animation, rect=None):
        super().__init__()
        self.id = id
        self.animation_handler = animation_handler
        self.current_animation_id = f'{self.id}_{current_animation}'
        self.current_animation = self.animation_handler.get_animation(self.current_animation_id)
        self.velocity = pygame.math.Vector2(0, 0)
        self.flipped = False
        self.collisions = {i:False for i in ['top', 'right', 'bottom', 'left']}
        self.colliding_rects = []

        if rect:
            self.set_rect(rect)
        else:
            self.rect = pygame.FRect(*position, *self.current_animation.image.get_size())
            self.offset = pygame.math.Vector2(0, 0)
                
    def draw(self, surface, scroll=[0,0], colorkey=None, vertical_flip=False, angle=0, position=None, visible_rect=None, alpha=None, animation_offset=None):
        if not self.is_visible(visible_rect):
            return
        if not position:
            position = self.position.copy()

        self.current_animation.render(surface, (position[0]-scroll.x, position[1]-scroll.y), [self.flipped, vertical_flip], colorkey, angle=angle, alpha=alpha, animation_offset=animation_offset)

        pygame.draw.rect(surface, (255,0,0), [self.rect[0]-scroll.x, self.rect[1]-scroll.y, self.rect[2], self.rect[3]], 1)

    def render_shadow(self, screen, scroll, position=None, size=None, offset=[0,0], color=(120, 120, 120)):
        if not position:
            position = [self.position[0], self.position[1]+self.image.get_height()*0.9]
        if not size:
            size = [self.image.get_width(), self.image.get_height()//5]

        shadow_surface = pygame.Surface(size)
        shadow_surface.convert_alpha()
        shadow_surface.fill((255, 255, 255))
        pygame.draw.ellipse(shadow_surface, color, (0, 0, *shadow_surface.get_size()))
        shadow_surface.set_colorkey((0, 0, 0))
        screen.blit(shadow_surface, (position[0]-scroll[0]-offset[0], position[1]-scroll[1]-offset[1]), special_flags=pygame.BLEND_RGBA_MULT)

    #Updates the animation
    def update(self, dt):
        self.colliding_rects.clear()
        self.current_animation.run(dt)

    def move(self, rects, dt):
        self.collisions = {k: False for k in ('top', 'right', 'bottom', 'left')}

        velocity = self.velocity * dt * self.game.window.fps * 3

        # horizontal movement and handling collision
        self.rect[0] += velocity.x
        hit_list = self.get_colliding_objects(rects)

        for rect in hit_list:
            if self.velocity.x > 0:
                self.rect.right = rect.left
                self.collisions['right'] = True

            if self.velocity.x < 0:
                self.rect.left = rect.right
                self.collisions['left'] = True

            if rect not in self.colliding_rects:
                self.colliding_rects.append(rect)


        # vertical movement and handling collision
        self.rect[1] += velocity.y
        hit_list = self.get_colliding_objects(rects)

        for rect in hit_list:
            if self.velocity.y > 0:
                self.rect.bottom = rect.top
                self.collisions['bottom'] = True

            if self.velocity.y < 0:
                self.rect.top = rect.bottom
                self.collisions['top'] = True

            if rect not in self.colliding_rects:
                self.colliding_rects.append(rect)

    # tells if the entity is visible
    def is_visible(self, visible_rect):
        if visible_rect == None:
            return True
        return pygame.Rect(*self.position, *self.image.get_size()).colliderect(visible_rect)
    
    def get_neighbour_tiles(self, ids):
        tile_pos = self.game.level.tilemap.get_on_grid_tile_position(self.rect.topleft)
        neighbour_tiles = self.game.level.tilemap.get_neighbour_tiles('collidable', tile_pos)

        return neighbour_tiles

    # UPDATE
    # returns the rects the player is colliding with
    def get_colliding_objects(self, rects):
        hit_list = []
        for rect in rects:
            if rect.colliderect(self.rect):
                hit_list.append(rect)

        return hit_list
    
    # sets the current animation of the entity
    def set_animation(self, animation, frame=None):
        if frame != None:
            self.current_animation.frame = frame

        animation = f'{self.id}_{animation}'

        if self.current_animation_id == animation:
            return

        if animation in self.animation_handler.animations:
            self.current_animation = self.animation_handler.get_animation(animation)
            self.current_animation_id = animation

    def set_position(self, position):
        # self.rect[0] = position[0] + self.offset[0]
        # self.rect[1] = position[1] + self.offset[1]
        self.rect.topleft = pygame.math.Vector2(*position) + self.offset

    def set_rect(self, rect):
        # self.offset = [rect[0], rect[1]]
        # self.rect[0] += rect[0]
        # self.rect[1] += rect[1]
        # self.rect[2] = rect.width
        # self.rect[3] = rect.height
        self.offset = pygame.math.Vector2(*rect.topleft)
        self.rect.topleft += self.offset
        self.rect[2] = rect.width
        self.rect[3] = rect.height

    def reset_rect(self):
        self.rect = pygame.Rect(*self.position, *self.current_animation.image.get_size())
        self.offset = pygame.math.Vector2(0, 0)

    def scale_rect(self, scale):
        self.rect.w *= scale
        self.rect.h *= scale

    #Flips the entity horizontally (when rendering only)
    def flip(self, bool):
        self.flipped = bool

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_size(self):
        return self.rect.size

    @property
    def position(self):
        # return [self.rect[0]-self.offset[0], self.rect[1]-self.offset[1]]
        return self.rect.topleft - self.offset

    @property
    def scale(self):
        return self.current_animation.animation_data.config['scale']

    #Returns the current animation's current image
    @property
    def image(self):
        return self.current_animation.image

    @property
    def center(self):
        return [self.rect[0]+self.get_width()/2, self.rect[1]+self.get_height()/2]

    @property
    def animation_center(self):
        return [self.position[0]+self.image.get_width()/2, self.position[1]+self.image.get_height()/2]

    @property
    def original_rect(self):
        return pygame.FRect(*self.position, *self.current_animation.image.get_size())