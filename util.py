import random
import math


def reverse(v):
    return scale_vector(v, -1)


def vector_op(vec_x, vec_y, op):
    return [op(x, y) for x, y in zip(vec_x, vec_y)]


def add_vector(vec_x, vec_y):
    return [x + y for x, y in zip(vec_x, vec_y)]


def scale_vector(vector, scalar):
    return [val * scalar for val in vector]


def random_vector(magnitude=1, dimensions=2):
    return [(random.random() - 0.5) * magnitude for _ in range(dimensions)]


def gauss_vector(vec, deviation):
    return [gauss(x, deviation) for x in vec]


def gauss(num, dev):
    return random.gauss(num, dev)


def separate_whole_decimal(vec):
    dec = [math.fmod(x, 1) for x in vec]
    whole = [int(x - d) for x, d in zip(vec, dec)]
    return whole, dec
