import pygame
import util
from operator import add, sub
import math


def fill_surface(color, surface):
    surface.fill(color)


"""
    todo: move the fade things out of here to their own class.
"""


class Drawable:
    def __init__(self, surface, location=None):
        self._original = surface
        self.angle = 0
        self.rect = self._original.get_rect()
        if location is not None:
            self.rect.move_ip(location)
        self._update_func = self._draw

        self.blink_time_total_remaining = 0
        self.blink_time_last = 0  # how long since the last blink in ms. < 0 means blinking, > 0 means going to blink
        self.blink_frequency = 0

        self.current_color = surface.get_at((0, 0))
        self.target_color = self.current_color
        self.amount_to_fade_per_milli = (0, 0, 0)
        self.fade_duration = 0
        self.draw_image_func = fill_surface
        self.buffered_fade = [0, 0, 0]

    def _update_func(self, actor_dict, window, delta_time):
        pass

    def fade(self, fade_duration, begin_color, end_color, draw_image_func=fill_surface):
        self.current_color = begin_color
        self.target_color = end_color
        self.fade_duration = fade_duration
        dif_vec = util.vector_op(begin_color, end_color, sub)
        self.amount_to_fade_per_milli = util.scale_vector(dif_vec, 1 / fade_duration)
        self.draw_image_func = draw_image_func
        self._update_func = self._fade

    def _fade(self, actor_dict, window, delta_time):
        self.fade_duration -= delta_time
        if self.fade_duration <= 0:
            self.current_color = self.target_color
            self._update_func = self._draw
        else:
            self.current_color = self._fade_get_next_color(delta_time)
            self.draw_image_func(self.current_color, self._original)
        self._draw(actor_dict, window, delta_time)

    def _fade_get_next_color(self, delta_time):
        delta_color = util.scale_vector(self.amount_to_fade_per_milli, delta_time)
        delta_color = util.vector_op(delta_color, self.buffered_fade, add)
        delta_color, self.buffered_fade = util.separate_whole_decimal(delta_color)
        return util.vector_op(self.current_color, delta_color, sub)

    def blink(self, time, frequency):
        self.blink_time_last = -frequency
        self.blink_frequency = frequency
        self.blink_time_total_remaining = time
        self._update_func = self._blink

    def _blink(self, actor_dict, window, delta_time):
        self.blink_time_total_remaining -= delta_time
        self.blink_time_last += delta_time
        if self.blink_time_total_remaining <= 0:
            self._update_func = self._draw
        if self.blink_time_last > 0:
            self._draw(actor_dict, window, delta_time)
            if self.blink_time_last > self.blink_frequency:
                self.blink_time_last = -self.blink_frequency

    def get_rect(self):
        return self.rect

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def update(self, actor_dict, window, delta_time):
        self._update_func(actor_dict, window, delta_time)

    def _draw(self, actor_dict, window, delta_time):
        image = pygame.transform.rotate(self._original, self.angle)
        window.blit(image, self.rect)

    def rotate(self, degrees):
        self.angle += degrees
