import pygame
import sys
from objects.asteroid import Asteroid
from objects.ship import Ship

"""
All weight is in kg.
All time is in ms.
All speed is in m/ms (p/ms)
"""

if __name__ == "__main__":
    pygame.init()

    size = width, height = 600, 600
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    ship = Ship()
    actors = [Asteroid(20), ship]

    move_map = {pygame.K_UP: ship.speed_up,
                pygame.K_DOWN: ship.speed_down,
                pygame.K_LEFT: ship.turn_left,
                pygame.K_RIGHT: ship.turn_right,
                pygame.K_SPACE: ship.fire_laser}

    clock = pygame.time.Clock()

    while 1:
        delta_time = clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pressed = pygame.key.get_pressed()
        for key, val in move_map.items():
            if pressed[key]:
                val(delta_time)

        screen.fill(black)

        newActors = []

        for actor in actors:
            actor.update(screen, delta_time)
            newActors = newActors + actor.get_actors()

        actors = newActors

        pygame.display.flip()
