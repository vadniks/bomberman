import sys
import pygame

from src.base_classes import Field
from src.base_classes import RGBScreen
from src.base_classes import MainMenu
from src.base_classes import Game_over
from src.sound  import Sounds


# это класс контроля игры
class Game:
    """
    Класс контроля игры - интерфейс, инициализация игры и остальные компаненты
    """

    def __init__(self, width=1280, height=720):
        """
        Создание карты

        :param width:
        :param height:
        """
        self.width = width
        self.height = height
        self.size = [self.width, self.height]
        self.game_over = False
        self.scen = 0
        self.library_init()
        self.objects = MainMenu()
        self.music = Sounds()
        # self.music.main_theme()
        # self.music.play_sound()

    # Инициализация библиотеки
    def library_init(self):
        """
        Отрисовка поля

        :return:
        """

        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size)

    def main_loop(self):
        """
        Основная программа - контроль меню, поля, экрана окончания игры

        :return:
        """
        while not self.game_over:  # Основной цикл работы программы
            if isinstance(self.objects, MainMenu) and not self.objects.start_game():
                self.music.stop_sound()
                self.music.main_theme()
                self.music.play_sound()
                self.objects = Field()
            if isinstance(self.objects, Field) and not self.objects.start_game():
                self.music.stop_sound()
                self.music.player_is_dead()
                self.music.play_sound()
                self.objects = Game_over(self.objects.end)
            if isinstance(self.objects, Game_over) and not self.objects.start_game():
                self.music.stop_sound()
                self.music.main_theme()
                self.music.play_sound()
                self.objects = MainMenu()

            self.process_events()
            self.process_logic()
            self.process_draw()

            pygame.time.wait(5)  # Ждать 10 миллисекунд

        sys.exit(0)  # Выход из программы

    def process_draw(self):
        """
        Заливка цветом фона приложения

        :return:
        """
        self.screen.fill(RGBScreen.BLACK)  # Заливка цветом
        self.objects.process_draw(self.screen)  # Должна быть у всех
        pygame.display.flip()  # Double buffering

    def process_logic(self):
        """
        Запуск логики объектов игры

        :return:
        """

        self.objects.process_logic()

    def process_events(self):
        """
        Обработка всех событий, происходящих в игре

        :return:
        """

        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:
                self.game_over = True
            self.objects.process_event(event)
