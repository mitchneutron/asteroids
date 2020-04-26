import pygame
import math
import objects.laser as lasermod
import objects.movable as movable
import objects.particle as particle
import util

fire_rate = 500
blink_frequency = 200
invincibility_max = 3500
max_hp = 3
dark_red = (139, 0, 0)
light_yellow = (255, 255, 0)


class Ship(movable.Movable):

    def __init__(self, location=None, hp=max_hp):
        self.particle_direction = 0
        self.particles_to_spawn = 0
        self.frequency = blink_frequency
        self.invincibility_max = invincibility_max
        self.invincibility_remaining = 0
        self.hp = hp
        self.max_hp = hp
        self.fire_rate = fire_rate  # fire every 500 ms
        self.last_fire = fire_rate  # time since last fire.
        self.lasers = []
        self.size = (10, 20)
        self.direction_vector = pygame.math.Vector2((0, -1))  # facing upwards
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        points = [(5, 0), (10, 20), (5, 15), (0, 20)]
        color = (230, 193, 150)
        pygame.draw.polygon(self.surface, color, points)
        super().__init__(self.surface, location=location, mass=300, drag=1)

    def fire_laser(self, delta_time):
        if self.last_fire >= self.fire_rate:
            # print("laser fired! " + str(delta_time))
            self.last_fire = 0
            location = self.get_rect().center
            laser = lasermod.Laser(location, self.direction_vector, self.get_velocity())
            self.lasers.append(laser)

    def hit(self, damage=1):
        if self.invincibility_remaining <= 0:
            self.hp -= damage
            self.invincibility_remaining = self.invincibility_max
            super().blink(self.invincibility_max, self.frequency)
            return True
        return False

    def speed_up(self, delta_time):
        self.increase_velocity(self.direction_vector, .001 * delta_time)
        self.particles_to_spawn += 3
        self.particle_direction = -1

    def speed_down(self, delta_time):
        self.particles_to_spawn += 1
        self.particle_direction = 1
        self.increase_velocity(self.direction_vector, -.0004 * delta_time)

    def turn_left(self, delta_time):
        self.rotate(.3 * delta_time)

    def turn_right(self, delta_time):
        self.rotate(-.3 * delta_time)

    def rotate(self, degrees):
        self.direction_vector = self.direction_vector.rotate(-degrees)
        super().rotate(degrees)

    def spawn_particles(self, destination_list):
        if self.particles_to_spawn <= 0:
            return
        location_offset = util.scale_vector(self.direction_vector, -3)
        location = util.add_vector(self.get_rect().center, location_offset)
        vel_offset = util.scale_vector(self.direction_vector, self.particle_direction)
        particle_velocity = util.add_vector(self.get_velocity(), vel_offset)
        particle.spawn_particles(destination_list, count=self.particles_to_spawn,
                                 location=location, base_velocity=particle_velocity,
                                 color=dark_red, fade_to_color=light_yellow)
        self.particles_to_spawn = 0

    def update(self, actor_dict, screen, delta_time):
        super().update(actor_dict, screen, delta_time)
        if self.hp <= 0:
            actor_dict.get(Ship).remove(self)
            return

        if self.last_fire <= self.fire_rate:
            actor_dict.get(lasermod.Laser).extend(self.lasers)
            self.lasers = []
            self.last_fire += delta_time

        if self.invincibility_remaining > 0:
            self.invincibility_remaining -= delta_time

        self.spawn_particles(actor_dict.get(particle.Particle))
