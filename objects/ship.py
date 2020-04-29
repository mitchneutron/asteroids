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
default_size = (20, 20)
default_points = [(10, 0), (15, 20), (10, 15), (5, 20)]
default_color = (230, 193, 150)


class Ship(movable.Movable):

    def __init__(self, location=None, hp=max_hp):
        self.particle_direction = 0
        self.engine_particles_to_spawn = 0
        self.hit_particles_to_spawn = 0
        self.frequency = blink_frequency
        self.invincibility_max = invincibility_max
        self.invincibility_remaining = 0
        self.hp = hp
        self.max_hp = hp
        self.fire_rate = fire_rate  # fire every 500 ms
        self.last_fire = fire_rate  # time since last fire.
        self.lasers = []
        self.size = default_size
        self.direction_vector = pygame.math.Vector2((0, -1))  # facing upwards
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        points = default_points
        self.color = default_color
        pygame.draw.polygon(self.surface, self.color, points)
        super().__init__(self.surface, location=location, mass=300, drag=1)

    def fire_laser(self, delta_time):
        if self.last_fire >= self.fire_rate:
            # print("laser fired! " + str(delta_time))
            self.last_fire = 0
            location = self.get_rect().center
            offset = util.scale_vector(self.direction_vector, 5)
            final_location = util.add_vector(offset, location)
            laser = lasermod.Laser(final_location, self.direction_vector, self.get_velocity())
            self.lasers.append(laser)

    def start_invincibility(self):
        self.invincibility_remaining = self.invincibility_max
        super().blink(self.invincibility_max, self.frequency)

    def hit(self, damage=1):
        if self.invincibility_remaining <= 0:
            self.hp -= damage
            self.hit_particles_to_spawn = damage * 5
            self.start_invincibility()
            return True
        return False

    def speed_up(self, delta_time):
        self.increase_velocity(self.direction_vector, .001 * delta_time)
        self.engine_particles_to_spawn += 3
        self.particle_direction = -1

    def speed_down(self, delta_time):
        self.engine_particles_to_spawn += 1
        self.particle_direction = 1
        self.increase_velocity(self.direction_vector, -.0004 * delta_time)

    def turn_left(self, delta_time):
        self.rotate(.3 * delta_time)

    def turn_right(self, delta_time):
        self.rotate(-.3 * delta_time)

    def rotate(self, degrees):
        self.direction_vector = self.direction_vector.rotate(-degrees)
        super().rotate(degrees)

    def spawn_death_particles(self, destination_list):
        particle.spawn_particles(destination_list=destination_list,
                                 count=100,
                                 location=self.get_rect().center,
                                 color=self.color,
                                 lifespan=100000,
                                 variation_velocity=0.1,
                                 variation_location=7,
                                 sway=0,
                                 diameter=5,
                                 drag=0.1,
                                 mass=100
                                 )

    def spawn_hit_particles(self, destination_list):
        if self.hit_particles_to_spawn <= 0:
            return
        particle.spawn_particles(destination_list=destination_list,
                                 count=self.hit_particles_to_spawn,
                                 location=self.get_rect().center,
                                 color=self.color,
                                 lifespan=300,
                                 variation_velocity=0.1,
                                 variation_location=7,
                                 sway=0,
                                 diameter=2,
                                 )
        self.hit_particles_to_spawn = 0

    def spawn_engine_particles(self, destination_list):
        if self.engine_particles_to_spawn <= 0:
            return
        location_offset = util.scale_vector(self.direction_vector, -3)
        location = util.add_vector(self.get_rect().center, location_offset)
        vel_offset = util.scale_vector(self.direction_vector, self.particle_direction)
        particle_velocity = util.add_vector(self.get_velocity(), vel_offset)
        particle.spawn_particles(destination_list, count=self.engine_particles_to_spawn,
                                 location=location, velocity=particle_velocity,
                                 color=dark_red, fade_to_color=light_yellow)
        self.engine_particles_to_spawn = 0

    def update(self, actor_dict, screen, delta_time):
        super().update(actor_dict, screen, delta_time)
        particle_list = actor_dict.get(particle.Particle)
        if self.hp <= 0:
            self.spawn_death_particles(particle_list)
            actor_dict.get(Ship).remove(self)
            return

        if self.last_fire <= self.fire_rate:
            actor_dict.get(lasermod.Laser).extend(self.lasers)
            self.lasers = []
            self.last_fire += delta_time

        if self.invincibility_remaining > 0:
            self.invincibility_remaining -= delta_time

        self.spawn_hit_particles(particle_list)
        self.spawn_engine_particles(particle_list)
