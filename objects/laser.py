from objects.movable import Movable
from objects.particle import Particle, spawn_particles
import pygame

lime_green = (50, 205, 50)
red = (200, 10, 10)
black = (0, 0, 0)
white = (255, 255, 255)


class Laser(Movable):
    def __init__(self, location, direction, base_velocity=(0, 0)):
        self.lifeSpan = 2000  # ms
        self.size = (8, 8)
        self.color = red
        surface = pygame.Surface(self.size)
        pygame.draw.circle(surface, self.color, (4, 4), 4)
        speed = 0.5
        velocity = [speed * direction[0] + base_velocity[0], speed * direction[1] + base_velocity[1]]
        super().__init__(surface, location, velocity, bounce=False)

    def spawn_laser_particle(self, particle_list):
        spawn_particles(destination_list=particle_list,
                        count=1,
                        location=self.get_rect().center,
                        color=self.color,
                        velocity=self.get_velocity(),
                        lifespan=100,
                        variation_velocity=0,
                        variation_location=0,
                        variation_color=0,
                        fade_to_color=black,
                        sway=0,
                        diameter=self.size[0],
                        )

    def collide_screen(self, screen):

        rect = self.get_rect()
        if rect.top < 0 or rect.bottom > screen.get_height() or rect.left < 0 or rect.right > screen.get_width():
            self.destroy()

    def spawn_laser_particles_for_death(self, particle_list):
        spawn_particles(destination_list=particle_list,
                        count=30,
                        location=self.get_rect().center,
                        color=white,
                        velocity=(0, 0),
                        lifespan=50,
                        variation_velocity=0.3,
                        variation_location=2,
                        variation_color=0,
                        sway=0.1
                        )

    def update(self, actor_dict, window, delta_time):
        super().update(actor_dict, window, delta_time)
        self.lifeSpan -= delta_time
        particles = actor_dict.get(Particle)
        if self.lifeSpan <= 0:
            actor_dict.get(Laser).remove(self)
            self.spawn_laser_particles_for_death(particles)
            return
        self.spawn_laser_particle(particles)


    def destroy(self):
        self.lifeSpan = 0

    def get_damage(self):
        return 100
