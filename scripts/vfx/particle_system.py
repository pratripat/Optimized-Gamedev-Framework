import pygame, math, random
from ..functions import normalize_vector, INITIAL_WINDOW_SIZE

class Particle_System:
    def __init__(self, game):
        self.game = game
        self.particles = pygame.sprite.Group()

        self.limit = math.inf
    
    def draw(self, surface, scroll=[0,0]):
        # self.particles.draw(surface, scroll)
        for particle in self.particles:
            particle.draw(surface, scroll)
    
    def update(self, dt, delete_off_screen_particles=True, delete_function=None):
        # updating the particles
        for particle in self.particles.sprites()[:]:
            particle.update(dt)
            # removing toberemoved particles
            if round(particle.radius) <= 0 or (delete_off_screen_particles and not particle.on_screen) or (delete_function != None and delete_function(particle)):
                self.particles.remove(particle)
                print('removed')
        
        # removes first few particles if there exists some limit
        if self.limit != math.inf:
            for i, particle in enumerate(list(self.particles)):
                if i >= self.limit: break

                self.particles.remove(particle)
                print('removed')
    
    def add_particles(self, number_of_particles, position, velocity, animation_id=None, color=(255,255,255), radius=3, decay_rate=2, normalize_rate=1):
        # if 'random' in velocity[0]:
        #     magnitude = eval(velocity[0].split('-'))
        #     print(magnitude)

        for _ in range(number_of_particles):
            particle = Particle(self.game, position, velocity, animation_id, color, radius, decay_rate, normalize_rate)
            self.particles.add(particle)
        
    def clear(self):
        self.particles.empty() # deletes all the sprites

    def set_limit(self, limit):
        self.limit = limit

class Particle(pygame.sprite.Sprite):
    def __init__(self, game, position, velocity, animation_id=None, color=(255,255,255), radius=10, decay_rate=2, normalize_rate=1):
        super().__init__()
        self.game = game
        self.rect = pygame.FRect(position[0], position[1], 10, 10)
        self.velocity = velocity
        self.animation = None

        if animation_id:
            self.animation = self.animation_handler.get_animation(self.current_animation_id)
        else:
            self.color = color
            self.radius = radius
            self.decay_rate = decay_rate
            self.normalize_rate_squared = normalize_rate**2
    
    def draw(self, surface, scroll=[0,0], colorkey=None, vertical_flip=False, angle=0, position=None, visible_rect=None, alpha=None, animation_offset=None, center=True):
        # if the particle has an animation, show that 
        if self.animation:
            self.animation.render(surface, (self.position[0]-scroll[0], self.position[1]-scroll[1]), [self.flipped, vertical_flip], colorkey, angle=angle, alpha=alpha, animation_offset=animation_offset)
        # else render the surface
        else:
            position = self.position
            if center: position = [self.position[0] - self.image.get_width()/2, self.position[1] - self.image.get_height()/2]

            surface.blit(self.image, (self.position[0] - scroll[0], self.position[1] - scroll[1]))
    
    def update(self, dt):
        self.rect[0] += self.velocity[0] * self.game.window.fps * dt
        self.rect[1] += self.velocity[1] * self.game.window.fps * dt

        if self.animation:
            self.animation.run(dt)
        else:
            self.radius -= random.uniform(0, self.decay_rate) * self.game.window.fps * dt

        self.velocity = normalize_vector(self.velocity, (self.velocity[0]**2 + self.velocity[1]**2)*(self.normalize_rate_squared))
    
    @property
    def image(self):
        if self.animation:
            return self.animation.image
        else:
            surface = pygame.Surface((2*self.radius, 2*self.radius)).convert()
            pygame.draw.circle(surface, self.color, (self.radius, self.radius), self.radius)
            surface.set_colorkey((0, 0, 0))
            return surface

    @property
    def on_screen(self):
        pos = [self.position[0]-self.game.camera.scroll[0], self.position[1]-self.game.camera.scroll[1]]
        return not (pos[0] < -self.image.get_width() or
                    pos[0] > INITIAL_WINDOW_SIZE[0]+self.image.get_width() or
                    pos[1] < -self.image.get_height() or
                    pos[1] > INITIAL_WINDOW_SIZE[1]+self.image.get_height())
    
    @property
    def position(self):
        return self.rect.topleft