import pygame
import sys


class Player:
    """
    Класс главного героя - нашего персонажа

    У персонажа есть здоровье и время до проигрыша
    Цель - убить приведений и найти дверь, спрятанную за рушимыми стенами
    """
    '''
    player_stand = pygame.image.load('res/images/animation_player/pygame_idle.png')
    player_walk_left = [
        pygame.image.load('../res/images/animation_player/pygame_left_1.png'),
        pygame.image.load('../res/images/animation_player/pygame_left_2.png'),
        pygame.image.load('../res/images/animation_player/pygame_left_3.png'),
        pygame.image.load('../res/images/animation_player/pygame_left_4.png'),
        pygame.image.load('../res/images/animation_player/pygame_left_5.png'),
        pygame.image.load('../res/images/animation_player/pygame_left_6.png')
    ]
    player_walk_right = [
        pygame.image.load('../res/images/animation_player/pygame_right_1.png'),
        pygame.image.load('../res/images/animation_player/pygame_right_2.png'),
        pygame.image.load('../res/images/animation_player/pygame_right_3.png'),
        pygame.image.load('../res/images/animation_player/pygame_right_4.png'),
        pygame.image.load('../res/images/animation_player/pygame_right_5.png'),
        pygame.image.load('../res/images/animation_player/pygame_right_6.png')
    ]
    '''

    def __init__(self, x, y):
        """
        Инициализация необходимых для персонажа параметров

        :param x:
        :param y:
        """

        self.rect = self.player_stand.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hero_died = False
        self.shift = 2
        self.shiftx = 0
        self.shifty = 0
        self.left = self.right = self.top = self.down = False
        self.animCount = 0

    def process_event(self, event):
        """
        Передвижение персонажа по карте

        :param event:
        :return:
        """

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self.right = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            self.top = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.down = True
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            self.left = False
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            self.right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_w:
            self.top = False
        if event.type == pygame.KEYUP and event.key == pygame.K_s:
            self.down = False
        self.dop(self.left, self.right, self.top, self.down)

    def dop(self, left, right, top, down):
        """
        Проверка на коллизию с концами карты

        :param left:
        :param right:
        :param top:
        :param down:
        :return:
        """
        if left:
            self.shiftx = -self.shift
        elif right:
            self.shiftx = self.shift
        else:
            self.shiftx = 0
            self.animCount = 0
        if top:
            self.shifty = -self.shift
        elif down:
            self.shifty = self.shift
        else:
            self.shifty = 0

    def process_logic(self):
        """
        Обработка передвижения

        :return:
        """

        self.rect.x += self.shiftx
        self.rect.y += self.shifty

    def process_draw(self, screen):
        """
        Отрисовка анимации в 9 этапов

        :param screen:
        :return:
        """

        if self.animCount + 1 >= 54:
            self.animCount = 0
        if self.left:
            screen.blit(self.player_walk_left[self.animCount // 9], self.rect)
            self.animCount += 1
        elif self.right:
            screen.blit(self.player_walk_right[self.animCount // 9], self.rect)
            self.animCount += 1
        else:
            screen.blit(self.player_stand, self.rect)

    def dead(self):
        """
        Обработка конца игры

        :return:
        """

        self.hero_died = True
        return self.hero_died
