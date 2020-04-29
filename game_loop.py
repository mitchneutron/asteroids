import pygame
import resource_manager
import random
import objects.asteroid
import objects.ship
import objects.laser
import objects.particle
import math

"""
All weight is in kg.
All time is in ms.
All speed is in m/ms (p/ms)
"""

black = 0, 0, 0
white = 255, 255, 255
lives = 1


def random_location(dims):
    return random.randrange(0, dims[0]), random.randrange(0, dims[1])


class GameLoop:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()

        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
        screen_rect = self.screen.get_rect()
        self.screen_size = screen_rect.w, screen_rect.h

        self.font_score = resource_manager.get_font(12)
        self.font_game_over = resource_manager.get_font(36)
        self.font_instructions = resource_manager.get_font(12)

        self.instructions = self.font_instructions.render("Arrow keys to move, space bar to fire, and ESC to exit",
                                                          False,
                                                          white)
        self.instructions_rect = self.instructions.get_rect()
        self.instructions_rect.bottomleft = screen_rect.bottomleft

        self.move_map = self.get_move_map()
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.actors = {objects.asteroid.Asteroid: [],
                       objects.ship.Ship: [],
                       objects.laser.Laser: [],
                       objects.particle.Particle: []}

        self.ship = None
        self.lives = lives
        self.level = 0
        self.score = 0
        self.playing = True

        self.spawn_ship()
        self.advance_level()

    def handle_collisions(self, actor_list):
        asteroids = {a: a.get_rect() for a in actor_list.get(objects.asteroid.Asteroid)}
        lasers = {l: l.get_rect() for l in actor_list.get(objects.laser.Laser)}
        ships = {s: s.get_rect() for s in actor_list.get(objects.ship.Ship)}

        for laser_entry in lasers.items():
            laser = laser_entry[0]
            rect = laser_entry[1]
            collision = rect.collidedict(asteroids, 1)
            if collision is not None:
                collision[0].hit(laser.get_damage())
                self.score += laser.get_damage()
                laser.destroy()

        for ship_entry in ships.items():
            ship = ship_entry[0]
            rect = ship_entry[1]
            collision = rect.collidedict(asteroids, 1)
            if collision is not None:
                if ship.hit():
                    collision[0].hit(10)

    def spawn_ship(self):
        ships = self.actors[objects.ship.Ship]
        if self.lives > 0 and not ships:
            self.ship = objects.ship.Ship((self.screen_size[0] / 2, self.screen_size[1] / 2))
            self.ship.start_invincibility()
            ships.append(self.ship)
            self.lives -= 1
        elif not ships:
            self.lives = -1

    def display_text(self):
        to_render = "Lives- " + str(self.lives + 1) + " Level- " + str(self.level) + " Score- " + str(self.score)
        rendered = self.font_score.render(to_render, False, white)
        self.screen.blit(rendered, rendered.get_rect())

        self.screen.blit(self.instructions, self.instructions_rect)

        if self.has_lost():
            self.display_game_over()


    def begin_loop(self):
        while self.playing:
            self.delta_time = self.clock.tick(60)
            self.spawn_ship()
            self.screen.fill(black)
            self.handle_events()
            self.handle_collisions(self.actors)
            self.update_actors(self.actors)
            self.display_text()
            if self.has_won():
                self.advance_level()
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

    def has_won(self):
        return len(self.actors.get(objects.asteroid.Asteroid)) <= 0

    def has_lost(self):
        return len(self.actors.get(objects.ship.Ship)) <= 0 and self.lives <= 0

    def advance_level(self):
        self.level += 1
        base_hp = int(math.log2(self.level * 20) + 15)
        for _ in range(self.level):
            asteroid = objects.asteroid.Asteroid(base_hp, location=random_location(self.screen_size))
            self.actors[objects.asteroid.Asteroid].append(asteroid)
        self.ship.start_invincibility()

    def display_game_over(self):
        message = self.font_game_over.render("Game Over", False, white)
        rect = message.get_rect()
        rect.center = self.screen.get_rect().center
        self.screen.blit(message, rect)




if __name__ == "__main__":
    pygame.init()
    loop = GameLoop()
    loop.begin_loop()
