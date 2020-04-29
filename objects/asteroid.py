import pygame
import objects.movable as movable
import objects.particle as particle
import util

brown = (139, 69, 19)
asteroid_color = brown
scalar = 4
total_asteroid_points_scalar = 2


def diameter_from_hp(hp):
    return hp * scalar + 5


def init_image(hp):
    # todo make the drawing cooler.
    direction_of_draw = pygame.math.Vector2((0, -1))
    total_points = hp + 2
    degrees_per_point = 360 / total_points
    diameter = diameter_from_hp(hp)
    radius = int(diameter / 2)
    surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    center_point = surface.get_rect().center
    points = []
    previous_scalar = radius
    for _ in range(total_points):
        point_scalar = max(min(util.gauss(previous_scalar + 1, 3), radius), 1)
        previous_scalar = point_scalar
        point = util.scale_vector(direction_of_draw, point_scalar)
        point = util.add_vector(point, center_point)
        points.append(point)
        direction_of_draw = direction_of_draw.rotate(degrees_per_point)

    pygame.draw.polygon(surface, asteroid_color, points)
    return surface

# todo: give the asteroid a weight based on the hp, and make the velocity more dynamic and
#  dependent on that.


class Asteroid(movable.Movable):
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
            velocity = util.random_vector()
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
            particles = actor_dict.get(particle.Particle)
            particle.spawn_particles(destination_list=particles,
                                     count=self.total_hp * 2,
                                     location=self.get_rect().center,
                                     color=brown,
                                     variation_location=int(diameter_from_hp(self.total_hp) / 4),
                                     variation_velocity=0.1,
                                     lifespan=1500,
                                     sway=0.00
                                     )

    def destroy(self):
        # break it into multiple asteroids. Randomize this...
        # maybe log base 2 of the size plus or minus a couple?
        self.destroyed = True
        remaining_hp_to_divvy = self.total_hp - 5
        while remaining_hp_to_divvy >= 1:
            self.children.append(Asteroid(remaining_hp_to_divvy, location=self.rect.center))
            remaining_hp_to_divvy -= 2

