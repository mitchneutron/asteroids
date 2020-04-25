import pygame, math, random
from objects.movable import Movable


def random_speed():
    return (random.randrange(0, 1) - 0.5) / 5, (random.randrange(0, 1) - 0.5) / 5


class Asteroid(Movable):
    def __init__(self, hp, velocity=None, location=None):
        self.total_hp = hp
        self.hp = hp
        self.destroyed = 0
        self.children = [self]

        surface = self.init_image(hp)

        if location is not None:
            surface.get_rect().center = location

        if velocity is None:
            velocity = random_speed()

        super().__init__(surface, velocity)

    def init_image(self, hp):
        # todo make the drawing cooler.
        color = (100, 150, 120)
        scalar = 4
        diameter = hp * scalar + 5
        radius = int(diameter / 2)
        surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (radius, radius), radius)
        return surface

    def hit(self, damage=1):
        self.hp -= damage
        if self.hp < 0:
            self.destroy()

    def get_actors(self):
        return self.children

    def destroy(self):
        # break it into multiple asteroids. Randomize this...
        # maybe log base 2 of the size plus or minus a couple?
        remaining_hp_to_divvy = self.total_hp - 5
        self.children = []
        while remaining_hp_to_divvy >= 1:
            self.children.append(Asteroid(remaining_hp_to_divvy, location=self.rect.center))
            remaining_hp_to_divvy -= 2

