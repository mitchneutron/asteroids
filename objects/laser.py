from objects.movable import Movable
import pygame


class Laser(Movable):
    def __init__(self, location, direction):
        self.lifeSpan = 2000  # ms
        size = (8, 8)
        red = (200, 0, 10)
        surface = pygame.Surface(size)
        surface.fill(red)
        speed = 0.5
        velocity = [speed * direction[0], speed * direction[1]]
        super().__init__(surface, location, velocity)

    def collide_screen(self, screen):
        rect = super().get_rect()
        if rect.top < 0 or rect.bottom > screen.get_height() or rect.left < 0 or rect.right > screen.get_width():
            self.lifeSpan = 0

    def update(self, actor_dict, window, delta_time):
        super().update(actor_dict, window, delta_time)
        self.lifeSpan -= delta_time
        if self.lifeSpan <= 0:
            print("removing laser!")
            actor_dict.get(Laser).remove(self)

    def destroy(self):
        self.lifeSpan = 0

    def get_damage(self):
        return 3
