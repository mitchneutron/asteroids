from objects.movable import Movable
import pygame
from main import random_velocity


def init_image(color, diameter):
    # todo make the drawing cooler.
    radius = int(diameter / 2)
    surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface


def spawn_particles(particle_list, base_velocity, variation, )


class Particle(Movable):
    def __init__(self, location, velocity=(0, 0), color=(0, 0, 0), diameter=3, drag=.05, mass=None, sway=1,
                 lifespan=3000):
        if mass is None:
            mass = diameter
        surface = init_image(color, diameter)
        self.sway = sway
        self.lifespan = lifespan
        super().__init__(surface, location, velocity, mass, drag)

    def update(self, actor_dict, screen, delta_time):
        velocity = random_velocity(self.sway)
        self.lifespan -= delta_time
        if self.lifespan <= 0:
            actor_dict.get(Particle).remove(self)
        super().increase_speed(velocity)
        super().update(actor_dict, screen, delta_time)
