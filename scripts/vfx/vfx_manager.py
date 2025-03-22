from .particle_system import Particle_System

class VFX:
    def __init__(self, game):
        self.game = game
        self.particle_system = Particle_System(self.game)
        self.overlay_particle_system = Particle_System(self.game)

    # these are rendered below the entities
    def render(self, surface, scroll=[0,0]):
        self.particle_system.draw(surface, scroll)

    # these are rendered above the entities
    def render_overlay_vfx(self, surface, scroll=[0,0]):
        self.overlay_particle_system.draw(surface, scroll)

    def update(self, dt):
        self.particle_system.update(dt)
        self.overlay_particle_system.update(dt)

    def clear(self):
        self.particle_system.clear()
        self.overlay_particle_system.clear()