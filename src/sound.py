import pygame
import sys


class Sounds:
    def __init__(self):
        pygame.mixer.init()

    def bomb_explosion_sound(self):
        pygame.mixer.music.load('sounds/bombexplosed.mp3')

    def got_points(self):
        pygame.mixer.music.load('sounds/points.mp3')

    def door_opened(self):
        pygame.mixer.music.load('sounds/door_opened.mp3')

    def player_is_dead(self):
        pygame.mixer.music.load('sounds/dead.mp3')

    def game_over(self):
        pygame.mixer.music.load('sounds/over.mp3')

    def level_passed(self):
        pygame.mixer.music.load('sounds/level_passed.mp3')

    def main_theme(self):
        pygame.mixer.music.load('sounds/theme.mp3')

    def play_sound(self):
        pygame.mixer.music.play()

    def stop_sound(self):
        pygame.mixer.music.stop()

def main():
    pygame.init()
    sc = pygame.display.set_mode((400, 400))
    a = Sounds()
    a.main_theme()
    a.play_sound()


if __name__ == "__main__":
    main()