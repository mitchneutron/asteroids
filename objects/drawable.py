import pygame


class Drawable:
    def __init__(self, image):
        self.original = image
        self.image = self.original
        self.angle = 0
        self.rect = self.original.get_rect()

    def get_rect(self):
        return self.rect

    def move(self, x, y):
        self.rect.move_ip(x, y)

    def update(self, window, delta_time):
        self.__draw(window)

    def __draw(self, window):
        window.blit(self.image, self.rect)

    def rotate(self, degrees):
        self.angle += degrees
        self.image = pygame.transform.rotate(self.original, self.angle)
