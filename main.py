import pygame
import sys
from objects.asteroid import Asteroid
from objects.ship import Ship


if __name__ == "__main__":
    pygame.init()

    size = width, height = 600, 600
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    ship = Ship()
    actors = [Asteroid(20, (1, 3)), ship]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     for actor in actors:
            #         actor.hit(5)
            if event.type == pygame.K_UP:
                ship.speed_up()
            if event.type == pygame.K_DOWN:
                ship.speed_down()
            if event.type == pygame.K_LEFT:
                ship.turn_left()
            if event.type == pygame.K_RIGHT:
                ship.turn_right()

        screen.fill(black)

        newActors = []

        for actor in actors:
            actor.update(screen)
            actor.draw(screen)
            newActors = newActors + actor.get_actors()

        actors = newActors

        pygame.display.flip()
