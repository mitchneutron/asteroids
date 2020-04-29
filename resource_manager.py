import pygame
import os


def get_font(size):
    if not pygame.get_init():
        pygame.init()

    if not pygame.font.get_init():
        print("Fonts are not initialized.")
        return None
    return pygame.font.Font(os.path.join('resources', 'font', '8-BIT WONDER.TTF'), size)
