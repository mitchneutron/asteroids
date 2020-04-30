import pygame
import os
import game_loop
import time
import functools
import game_loop
import resource_manager

white = 255, 255, 255
black = 0, 0, 0
tick_size = 10, 10
tick_points = [(0, 0), (10, 5), (0, 10)]
menu_spacing = 5

tick = pygame.Surface(tick_size)
pygame.draw.polygon(tick, white, tick_points)

class MainMenu:
    def __init__(self):
        if not pygame.get_init():
            pygame.init()

        self.playing = True
        self.clock = pygame.time.Clock()

        self.size = 400, 400
        self.screen = pygame.display.set_mode(self.size)

        self.font = resource_manager.get_font(24)
        self.text_start_game = self.font.render("Start Game", False, white)
        # todo: one day.
        # self.text_high_scores = self.font.render("View High Scores", False, white)
        self.text_quit = self.font.render("Quit", False, white)

        self.menu_items = [self.text_start_game, self.text_quit]
        self.menu_options_map = self.get_options_map()
        self.menu_item_rect_map = self.get_menu_item_rect_map(self.menu_items)
        self.key_map = self.get_key_map()

        self.selected_index = 0
        self.tick_rect = tick.get_rect()
        self.tick_blink_frequency = 300
        self.tick_blink_time = -self.tick_blink_frequency
        self.move_tick()

    def get_menu_item_rect_map(self, menu_items):
        rect_dict = {item: item.get_rect() for item in menu_items}
        heights = map(lambda x: x.h, rect_dict.values())
        total_height = functools.reduce(lambda x, y: x + y, heights)
        total_height += menu_spacing * (len(menu_items) - 1)
        # we want to center it around the center of the menu
        top_height = (self.size[1] - total_height) / 2
        center_x = self.size[0] / 2
        next_height = top_height
        for rect in rect_dict.values():
            rect.centerx = center_x
            rect.top = next_height
            next_height += menu_spacing + rect.height
        return rect_dict

    def start_game(self):
        pygame.display.quit()
        game = game_loop.GameLoop()
        game.begin_loop()
        if pygame.display.get_init():
            pygame.display.quit()
        pygame.display.init()
        self.screen = pygame.display.set_mode(self.size)
        pass

    def view_high_scores(self):
        pass

    def quit(self):
        self.playing = False

    def get_options_map(self):
        return {
            self.text_start_game: self.start_game,
            # self.text_high_scores: self.view_high_scores,
            self.text_quit: self.quit
        }

    def option_up(self):
        self.selected_index -= 1
        if self.selected_index < 0:
            self.selected_index = len(self.menu_items) - 1
        self.move_tick()

    def option_down(self):
        self.selected_index += 1
        if self.selected_index >= len(self.menu_items):
            self.selected_index = 0
        self.move_tick()

    def move_tick(self):
        selected_option_rect = self.menu_item_rect_map[self.menu_items[self.selected_index]]
        center = selected_option_rect.left - 20, selected_option_rect.centery
        self.tick_rect.center = center
        self.tick_blink_time = 0

    def select(self):
        self.menu_options_map[self.menu_items[self.selected_index]]()

    def get_key_map(self):
        return {pygame.K_UP: self.option_up,
                pygame.K_DOWN: self.option_down,
                pygame.K_RETURN: self.select,
                pygame.K_KP_ENTER: self.select,
                pygame.K_ESCAPE: self.quit}

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key in self.key_map:
                    self.key_map[event.key]()

    def draw_tick(self, delta_time):
        self.tick_blink_time += delta_time
        if self.tick_blink_time > 0:
            self.screen.blit(tick, self.tick_rect)
            if self.tick_blink_time > self.tick_blink_frequency:
                self.tick_blink_time = - self.tick_blink_frequency

    def draw_menu_items(self):
        for image, rect in self.menu_item_rect_map.items():
            self.screen.blit(image, rect)

    def run(self):

        while self.playing:
            self.handle_events()
            delta_time = self.clock.tick(60)
            self.screen.fill(black)
            self.draw_menu_items()
            self.draw_tick(delta_time)
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    menu = MainMenu()
    menu.run()
