from objects.movable import Movable
import pygame


class Laser(Movable):
    def __init__(self, location, direction, base_velocity=(0, 0)):
        self.lifeSpan = 2000  # ms
        size = (8, 8)
        red = (200, 0, 10)
        surface = pygame.Surface(size)
        surface.fill(red)
        speed = 0.5
        velocity = [speed * direction[0] + base_velocity[0], speed * direction[1] + base_velocity[1]]
        super().__init__(surface, location, velocity, bounce=False)

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
