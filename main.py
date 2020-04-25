import pygame
import sys
import random
from objects.asteroid import Asteroid
from objects.ship import Ship
from objects.laser import Laser
from objects.particle import Particle
from constants import *

"""
All weight is in kg.
All time is in ms.
All speed is in m/ms (p/ms)
"""


def random_velocity(magnitude=1):
    return (random.random() - 0.5) * magnitude, (random.random() - 0.5) * magnitude


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pressed = pygame.key.get_pressed()
    for key, val in move_map.items():
        if pressed[key]:
            val(ship, delta_time)


def get_move_map():
    return {pygame.K_UP: lambda obj, args: obj.speed_up(args),
            pygame.K_DOWN: lambda obj, args: obj.speed_down(args),
            pygame.K_LEFT: lambda obj, args: obj.turn_left(args),
            pygame.K_RIGHT: lambda obj, args: obj.turn_right(args),
            pygame.K_SPACE: lambda obj, args: obj.fire_laser(args)}


def refresh_actor_list(actor_list):
    new_actor_list = []
    for actor in actor_list:
        new_actor_list = new_actor_list + actor.update(screen, delta_time)
    return new_actor_list


def handle_collisions(actor_list):
    asteroids = {a: a.get_rect() for a in actor_list.get(Asteroid)}
    lasers = {l: l.get_rect() for l in actor_list.get(Laser)}
    ships = {s: s.get_rect() for s in actor_list.get(Ship)}

    for laser_entry in lasers.items():
        laser = laser_entry[0]
        rect = laser_entry[1]
        collision = rect.collidedict(asteroids, 1)
        if collision is not None:
            collision[0].hit(laser.get_damage())
            laser.destroy()

    for ship_entry in ships.items():
        ship = ship_entry[0]
        rect = ship_entry[1]
        collision = rect.collidedict(asteroids, 1)
        if collision is not None:
            if ship.hit():
                collision[0].hit(10)


def update_actors(actor_dict):
    for actor_list in actor_dict.values():
        for actor in actor_list:
            actor.update(actor_dict, screen, delta_time)


def random_location(dims):
    return random.randrange(0, dims[0]), random.randrange(0, dims[1])


if __name__ == "__main__":
    pygame.init()

    size = width, height = 600, 600
    speed = [2, 2]
    black = 0, 0, 0
    screen = pygame.display.set_mode(size)
    move_map = get_move_map()
    clock = pygame.time.Clock()

    ship = Ship(random_location(size))
    asteroid = Asteroid(20, location=random_location(size))
    actors = {Asteroid: [asteroid],
              Ship: [ship],
              Laser: [],
              Particle: []}

    while 1:
        delta_time = clock.tick(60)
        screen.fill(black)
        handle_events()
        handle_collisions(actors)
        update_actors(actors)
        pygame.display.flip()
