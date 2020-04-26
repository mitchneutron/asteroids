import objects.movable
import pygame
import util

default_drag = 0.5
default_mass = 50
default_diameter = 3
default_color = (255, 255, 255)
default_lifespan = 100
default_sway = 0.1
default_variation = 0.1


def spawn_particles(destination_list, count, location, color=default_color, variation=default_variation, base_velocity=(0, 0),
                    sway=default_sway, size=default_diameter, drag=default_drag,
                    lifespan=default_lifespan, mass=default_mass, fade_to_color=None):
    for x in range(count):
        velocity = util.gauss_vector(base_velocity, variation)
        location = util.gauss_vector(location, variation)
        particle = Particle(location, velocity, color, size, drag, mass, sway, lifespan, fade_to_color=fade_to_color)
        destination_list.append(particle)


class Particle(objects.movable.Movable):
    def __init__(self, location, velocity=(0, 0), color=default_color, diameter=default_diameter,
                 drag=default_drag, mass=None, sway=default_sway, lifespan=default_lifespan, fade_to_color=None):
        lifespan = util.gauss(lifespan, sway * 2000)
        if mass is None:
            mass = diameter

        radius = int(diameter / 2)
        surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)

        def draw_func(color, surface, rad=radius):
            pygame.draw.circle(surface, color, (rad, rad), rad)

        draw_func(color, surface)

        self.sway = sway
        self.lifespan = lifespan
        velocity = velocity[0], velocity[1]
        super().__init__(surface, location=location, velocity=velocity, mass=mass, drag=drag, bounce=False)
        if fade_to_color is not None:
            self.fade(lifespan, color, fade_to_color, draw_func)



    def update(self, actor_dict, screen, delta_time):
        velocity_change = util.gauss_vector((0, 0), self.sway)
        self.lifespan -= delta_time
        if self.lifespan <= 0:
            actor_dict.get(Particle).remove(self)
        super().increase_velocity(velocity_change)
        super().update(actor_dict, screen, delta_time)
