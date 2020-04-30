import pygame
import sys
import os


def get_font(size):
    if not pygame.get_init():
        pygame.init()
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(application_path, "resources", "font", "8-BITWONDER.TTF")

    if not pygame.font.get_init():
        print("Fonts are not initialized.")
        return None
    return pygame.font.Font(file_path, size)
