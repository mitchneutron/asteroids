import pygame
from objects.actor import Actor
from objects.laser import Laser
from objects.movable import Movable
from objects.drawable import Drawable


class Ship(Movable):
    def __init__(self):
        self.fire_rate = 500  # fire every 500 ms
        self.last_fire = 500  # time since last fire.
        self.lasers = []
        self.size = (10, 20)
        self.direction_vector = pygame.math.Vector2((0, -1))  # facing upwards
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        points = [(5, 0), (10, 20), (5, 15), (0, 20)]
        color = (230, 193, 150)
        pygame.draw.polygon(self.surface, color, points)
        super().__init__(self.surface, mass=300, drag=1)

    def get_actors(self):
        children = self.lasers
        children.append(self)
        return children

    def fire_laser(self, delta_time):
        if self.last_fire >= self.fire_rate:
            rect = self.get_rect()
            laser = Laser(rect.center, self.direction_vector)
            self.lasers.append(laser)
            self.last_fire = 0

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

    def update(self, screen, delta_time):
        super().update(screen, delta_time)
        if self.last_fire <= self.fire_rate:
            self.last_fire += delta_time
