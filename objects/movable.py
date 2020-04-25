import math
from objects.actor import Actor

# speed will be pixels/millisecond


class Movable(Actor):
    def __init__(self, surface, velocity=None, mass=None, drag=0):
        self.mass = mass
        self.velocity_vector = [0, 0]
        self.drag = drag
        if velocity is not None:
            self.velocity_vector[0] = velocity[0]
            self.velocity_vector[1] = velocity[1]
        self.buffered_move = [0.0, 0.0]  # move that I haven't made because we can only move in full pixels.
        super().__init__(surface)

    def increase_speed(self, vector, magnitude=1):
        self.velocity_vector[0] += vector[0] * magnitude
        self.velocity_vector[1] += vector[1] * magnitude

    def set_speed(self, vector):
        self.velocity_vector[0] = vector[0]
        self.velocity_vector[1] = vector[1]

    def scale_speed(self, scalar):
        self.velocity_vector[0] *= scalar
        self.velocity_vector[1] *= scalar

    def change_sign_x(self, sign):
        self.velocity_vector[0] = sign * abs(self.velocity_vector[0])
        self.buffered_move[0] = sign * abs(self.buffered_move[0])

    def change_sign_y(self, sign):
        self.velocity_vector[1] = sign * abs(self.velocity_vector[1])
        self.buffered_move[1] = sign * abs(self.buffered_move[1])

    def collide_screen(self, screen):
        rect = super().get_rect()
        if rect.top < 0:
            self.change_sign_y(1)
            rect.top = 0
        elif rect.bottom > screen.get_height():
            self.change_sign_y(-1)
            rect.bottom = screen.get_height()
        if rect.left < 0:
            self.change_sign_x(1)
            rect.left = 0
        elif rect.right > screen.get_width():
            self.change_sign_x(-1)
            rect.right = screen.get_width()

#  f = ma
#  v = at
    def apply_drag(self, delta_time):
        if self.drag is not 0:
            v = self.velocity_vector
            fx = ((v[0] ** 2) / 2) * self.drag * math.copysign(1, v[0])
            fy = ((v[1] ** 2) / 2) * self.drag * math.copysign(1, v[1])
            ax = fx / self.mass
            ay = fy / self.mass
            v[0] -= ax * delta_time
            v[1] -= ay * delta_time

    def _apply_velocity(self, delta_time):
        x = (self.velocity_vector[0] * delta_time) + self.buffered_move[0]
        y = (self.velocity_vector[1] * delta_time) + self.buffered_move[1]
        self.buffered_move[0] = math.fmod(x, 1)
        self.buffered_move[1] = math.fmod(y, 1)
        self.move(int(x - self.buffered_move[0]), int(y - self.buffered_move[1]))

    def update(self, screen, delta_time):
        self.collide_screen(screen)
        self.apply_drag(delta_time)
        self._apply_velocity(delta_time)
        super().update(screen, delta_time)

    # No collisions and physics yet.
    # def calculate_momentum(self):
    #     return [(x * self.weight, y * self.weight) for x, y in self.speed]
    #
    # def calculate_elasticity(self, other):
    #     return (self.elasticity * self.weight + other.elasticity * other.weight) / (self.weight + other.weight)
    #
    # def collide(self, other):
    #     # calculate total momentum.
    #     momentum_vector = tuple(map(sum, zip(self.calculate_momentum(), other.calculate_momentum())))
    #     # get average elasticity
    #     average_elasticity = self.calculate_elasticity(other)
    #     # just update the speed of this guy. Every collide should be responsible for updating itself.
    #






