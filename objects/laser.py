from objects.movable import Movable
import pygame


class Laser(Movable):
    def __init__(self, location, direction):
        self.lifeSpan = 4000  # 4 seconds
        size = (8, 8)
        red = (200, 0, 10)
        surface = pygame.Surface(size)
        surface.fill(red)
        surface.get_rect().center = location
        speed = 2
        velocity = direction
        velocity[0] *= speed
        velocity[1] *= speed
        super().__init__(surface, velocity)

    def collide_screen(self, screen):
        rect = super().get_rect()
        if rect.top < 0 or rect.bottom > screen.get_height() or rect.left < 0 or rect.right > screen.get_width():
            self.lifeSpan = 0

    def get_actors(self):
        if self.lifeSpan <= 0:
            return []
        return [self]

    def update(self, window, delta_time):
        self.lifeSpan -= delta_time
        super().update(window, delta_time)
