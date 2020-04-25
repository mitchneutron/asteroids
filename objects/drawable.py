import pygame


class Drawable:
    def __init__(self, image, location=None):
        self.blinking = False
        self.blink_time_total_remaining = 0
        self.blink_time_last = 0  # how long since the last blink in ms. < 0 means blinking, > 0 means going to blink
        self.blink_frequency = 0
        self.original = image
        self.image = self.original
        self.angle = 0
        self.rect = self.original.get_rect()
        if location is not None:
            self.rect.move_ip(location)

    def blink(self, time, frequency):
        self.blink_time_last = -frequency
        self.blink_frequency = frequency
        self.blink_time_total_remaining = time
        self.blinking = True

    def get_rect(self):
        return self.rect

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def update(self, actor_dict, window, delta_time):
        if self.blinking:
            self.blink_time_total_remaining -= delta_time
            self.blink_time_last += delta_time
            if self.blink_time_total_remaining <= 0:
                self.blinking = False
            if self.blink_time_last > 0:
                self.__draw(window)
                if self.blink_time_last > self.blink_frequency:
                    self.blink_time_last = -self.blink_frequency
        else:
            self.__draw(window)

    def __draw(self, window):
        window.blit(self.image, self.rect)

    def rotate(self, degrees):
        self.angle += degrees
        self.image = pygame.transform.rotate(self.original, self.angle)
