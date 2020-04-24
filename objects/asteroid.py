import pygame, math, random
from objects.actor import Actor


def random_speed():
    return math.floor((random.randrange(0, 4) - 2)),\
           math.floor((random.randrange(0, 4) - 2))


class Asteroid(Actor):
    def __init__(self, hp, speed, location=None):
        self.color = (100, 150, 120)
        self.speed = [speed[0], speed[1]]
        self.scalar = 4
        self.diameter = hp * self.scalar + 5
        self.radius = int(self.diameter / 2)
        self.size = (self.diameter, self.diameter)
        self.total_hp = hp
        self.hp = hp
        self.surface = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        if location is not None:
            self.rect.center = location

        self.destroyed = 0
        self.children = [self]
        # just gotta make the thing look different based on size and hp.
        self.init_image()

    def init_image(self):
        # todo make the drawing cooler.
        pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)
        super().__init__(self.surface, self.rect)

    def update(self, screen):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > screen.get_width():
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > screen.get_height():
            self.speed[1] = -self.speed[1]

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
        list = []
        while remaining_hp_to_divvy >= 1:
            list.append(Asteroid(remaining_hp_to_divvy, random_speed(), self.rect.center))
            remaining_hp_to_divvy -= 2
        self.children = list

