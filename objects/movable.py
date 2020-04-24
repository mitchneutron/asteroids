import math


class Movable:
    def __init__(self, rect):
        self.velocity_vector = [0, 0]
        self.buffered_move = [0, 0]  # move that I haven't made because we can only move in full pixels.
        self.rect = rect

    def increase_speed(self, vector):
        self.velocity_vector[0] += vector[0]
        self.velocity_vector[1] += vector[1]

    def increase_speed(self, vector, magnitude):
        self.velocity_vector[0] += vector[0] * magnitude
        self.velocity_vector[1] += vector[1] * magnitude

    def update(self):
        x, self.buffered_move[0] = math.modf(self.velocity_vector[0] + self.buffered_move[0])
        y, self.buffered_move[1] = math.modf(self.velocity_vector[1] + self.buffered_move[1])
        self.rect.move_ip(x, y)

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






