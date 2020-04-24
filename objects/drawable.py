import pygame


class Drawable:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

    def draw(self, window):
        window.blit(self.image, self.rect)
