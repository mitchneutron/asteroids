import pygame
import sys
import random
import objects.asteroid
import objects.ship
import objects.laser
import objects.particle

"""
All weight is in kg.
All time is in ms.
All speed is in m/ms (p/ms)
"""

black = 0, 0, 0


def handle_collisions(actor_list):
    asteroids = {a: a.get_rect() for a in actor_list.get(objects.asteroid.Asteroid)}
    lasers = {l: l.get_rect() for l in actor_list.get(objects.laser.Laser)}
    ships = {s: s.get_rect() for s in actor_list.get(objects.ship.Ship)}

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


def random_location(dims):
    return random.randrange(0, dims[0]), random.randrange(0, dims[1])


class GameLoop:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()

        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        rect = self.screen.get_rect()
        size = rect.w, rect.h

        self.move_map = self.get_move_map()
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.ship = objects.ship.Ship((size[0] / 2, size[1] / 2))
        asteroid = objects.asteroid.Asteroid(20, location=random_location(size))
        self.actors = {objects.asteroid.Asteroid: [asteroid],
                       objects.ship.Ship: [self.ship],
                       objects.laser.Laser: [],
                       objects.particle.Particle: []}

        self.playing = True

    def begin_loop(self):
        while self.playing:
            self.delta_time = self.clock.tick(60)
            self.screen.fill(black)
            self.handle_events()
            handle_collisions(self.actors)
            self.update_actors(self.actors)
            pygame.display.flip()

    def update_actors(self, actor_dict):
        for actor_list in actor_dict.values():
            for actor in actor_list:
                actor.update(actor_dict, self.screen, self.delta_time)

    def refresh_actor_list(self, actor_list):
        new_actor_list = []
        for actor in actor_list:
            new_actor_list = new_actor_list + actor.update(self.screen, self.delta_time)
        return new_actor_list

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

        pressed = pygame.key.get_pressed()
        for key, func in self.move_map.items():
            if pressed[key]:
                func()

    def get_move_map(self):
        return {pygame.K_UP: lambda: self.ship.speed_up(self.delta_time),
                pygame.K_DOWN: lambda: self.ship.speed_down(self.delta_time),
                pygame.K_LEFT: lambda: self.ship.turn_left(self.delta_time),
                pygame.K_RIGHT: lambda: self.ship.turn_right(self.delta_time),
                pygame.K_SPACE: lambda: self.ship.fire_laser(self.delta_time),
                pygame.K_ESCAPE: self.finish_playing}

    def finish_playing(self):
        self.playing = False


if __name__ == "__main__":
    pygame.init()
    loop = GameLoop()
    loop.begin_loop()



