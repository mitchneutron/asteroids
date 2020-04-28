import objects.movable
import pygame
import util

default_drag = 0.5
default_mass = 50
default_diameter = 3
default_color = (255, 255, 255)
default_lifespan = 100
default_sway = 0.1
default_variation_speed = 0.05
default_variation_location = 3
default_variation_color = 0


def vary_color(color, variation):
    color = util.gauss_vector(color, variation)
    color = [min(255, max(0, int(x))) for x in color]
    return color


def spawn_particles(destination_list,
                    count,
                    location,
                    color=default_color,
                    velocity=(0, 0),
                    lifespan=default_lifespan,
                    variation_velocity=default_variation_speed,
                    variation_location=default_variation_location,
                    variation_color=default_variation_color,
                    fade_to_color=None,
                    mass=default_mass,
                    sway=default_sway,
                    diameter=default_diameter,
                    drag=default_drag,
                    ):
    for x in range(count):
        particle_color = vary_color(color, variation_color)
        particle_velocity = util.gauss_vector(velocity, variation_velocity)
        particle_location = util.gauss_vector(location, variation_location)
        if fade_to_color is not None:
            fade_to_color = vary_color(fade_to_color, variation_color)
        particle = Particle(particle_location, particle_velocity,
                            particle_color, diameter, drag, mass,
                            sway, lifespan, fade_to_color=fade_to_color)
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
