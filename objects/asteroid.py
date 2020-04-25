import pygame, math, random
from objects.movable import Movable


def random_speed():
    return (random.random() - 0.5), (random.random() - 0.5)


def init_image(hp):
    # todo make the drawing cooler.
    color = (100, 150, 120)
    scalar = 4
    diameter = hp * scalar + 5
    radius = int(diameter / 2)
    surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radius, radius), radius)
    return surface

# todo: give the asteroid a weight based on the hp, and make the velocity more dynamic and
#  dependent on that.


class Asteroid(Movable):
    def __init__(self, hp, velocity=None, location=None):
        self.total_hp = hp
        self.hp = hp
        self.destroyed = 0
        self.children = []
        self.destroyed = False

        surface = init_image(hp)

        if location is not None:
            rect = surface.get_rect()
            rect.center = location

        if velocity is None:
            scalar = 1.5
            velocity = random_speed()
            velocity = (velocity[0] * scalar / (hp + 3), velocity[1] * scalar / (hp + 3))

        super().__init__(surface, velocity=velocity, location=location)

    def hit(self, damage=1):
        self.hp -= damage
        if self.hp < 0:
            self.destroy()

    def update(self, actor_dict, screen, delta_time):
        super().update(actor_dict, screen, delta_time)
        if self.destroyed:
            asteroids = actor_dict.get(Asteroid)
            asteroids.remove(self)
            asteroids.extend(self.children)

    def destroy(self):
        # break it into multiple asteroids. Randomize this...
        # maybe log base 2 of the size plus or minus a couple?
        self.destroyed = True
        remaining_hp_to_divvy = self.total_hp - 5
        while remaining_hp_to_divvy >= 1:
            self.children.append(Asteroid(remaining_hp_to_divvy, location=self.rect.center))
            remaining_hp_to_divvy -= 2

