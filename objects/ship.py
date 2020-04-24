import pygame
from objects.actor import Actor
from objects.movable import Movable
from objects.drawable import Drawable


class Ship(Movable, Actor):
    def __init__(self):
        self.size = (10, 20)
        self.direction_vector = pygame.math.Vector2((0, -1))  # facing upwards
        self.angle = 0
        self.buffered_move = [0, 0]  # move that I haven't made because we can only move in full pixels.
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.original = self.surface
        points = [(5, 0), (10, 20), (5, 15), (0, 20)]
        color = (230, 193, 150)
        self.rect = self.surface.get_rect()
        pygame.draw.polygon(self.surface, color, points)
        Movable.__init__(self, self.rect)
        Drawable.__init__(self, self.surface, self.rect)

    def update(self, screen):
        Movable.update(self)
        Actor.update(self, screen)

#  360/5 points of turning we can be on. so 72 in total to make a full circle.
    def speed_up(self):
        self.increase_speed(self.direction_vector, 0.1)

    def speed_down(self):
        self.increase_speed(self.direction_vector, -0.1)

    def turn_left(self):
        self._rotate(360/5)

    def turn_right(self):
        self._rotate(-360/5)

    def __rotate(self, degrees):
        self.angle += degrees
        self.surface = pygame.transform.rotate(self.original, self.angle)
        self.direction_vector = self.direction_vector.rotate(degrees)
