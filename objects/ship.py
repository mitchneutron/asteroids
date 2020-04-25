import pygame
from objects.actor import Actor
from objects.laser import Laser
from objects.movable import Movable
from objects.drawable import Drawable


class Ship(Movable):

    def __init__(self, location=None, hp=3):
        self.frequency = 200
        self.max_invincibility_time = 5000
        self.invincibility = 0
        self.hp = hp
        self.max_hp = self.hp
        self.fire_rate = 500  # fire every 500 ms
        self.last_fire = 500  # time since last fire.
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
            laser = Laser(location, self.direction_vector)
            self.lasers.append(laser)

    def hit(self, damage=1):
        if self.invincibility <= 0:
            self.hp -= damage
            self.invincibility = self.max_invincibility_time
            super().blink(self.max_invincibility_time, self.frequency)
            return True
        return False

    def speed_up(self, delta_time):
        self.increase_speed(self.direction_vector, .001 * delta_time)

    def speed_down(self, delta_time):
        self.increase_speed(self.direction_vector, -.001 * delta_time)

    def turn_left(self, delta_time):
        self.rotate(.3 * delta_time)

    def turn_right(self, delta_time):
        self.rotate(-.3 * delta_time)

    def rotate(self, degrees):
        self.direction_vector = self.direction_vector.rotate(-degrees)
        super().rotate(degrees)

    def update(self, actor_dict, screen, delta_time):
        super().update(actor_dict, screen, delta_time)
        if self.hp <= 0:
            actor_dict.get(Ship).remove(self)
            return
        if self.last_fire <= self.fire_rate:
            actor_dict.get(Laser).extend(self.lasers)
            self.lasers = []
            self.last_fire += delta_time
        if self.invincibility > 0:
            self.invincibility -= delta_time
