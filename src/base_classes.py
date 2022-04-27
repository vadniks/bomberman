import pygame
from random import randint
from random import randrange

# Библиотека классов
class Game_over:
    def __init__(self, end):
        self.game_over = True
        self.time = 500
        self.end = end

    def process_logic(self):
        if self.time < 0:
            self.game_over = False
        self.time -= 1

    def start_game(self):
        return self.game_over

    def process_event(self,event):
        pass

    def process_draw(self, screen):
        if self.end:
            screen.fill(RGBScreen.WHITE)
            Text_lifes = pygame.font.SysFont('Comic Sans MS', 72, True, False).render('You WIN ', True, [0, 0, 128])
            screen.blit(Text_lifes, [480, 300])
        else:
            screen.fill(RGBScreen.BLACK)
            Text_lifes = pygame.font.SysFont('Comic Sans MS', 72, True, False).render('Game over ', True, [128, 0, 0])
            screen.blit(Text_lifes, [480, 300])


class BreakWall:
    sprite = pygame.image.load('images/WallBrack.png')

    def __init__(self, x, y):
        self.enable = True
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def process_draw(self, screen):
        if self.enable:
            screen.blit(self.sprite, self.rect)

    def process_event(self, event):
        pass

    def process_logic(self):
        pass


class UnBreakWall:
    sprite = pygame.image.load('images/WallUnbrack.png')

    def __init__(self, x, y):
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def process_draw(self, screen):
        screen.blit(self.sprite, self.rect)

    def process_event(self, event):
        pass

    def process_logic(self):
        pass


class Field:
    def __init__(self):
        self.x = 0  # абсцисса начала поля
        self.y = 101  # ордината начала поля
        self.wight = 23  # ширина поля
        self.height = 11  # высота поля
        self.size = 57  # расстояние между блоками
        self.rect = pygame.Rect(self.x, self.y, 500, 500)
        self.BWcount = 30
        self.GhostsBotscount = 5
        self.UnbrackWalls = []
        self.BrackWalls = []
        self.Player = Player(5 * self.size, 5 * self.size)
        self.Bomb = Bomb(55, 155)
        self.Fire = Fire(0, 0)
        self.Door = Door(355, 155)
        self.PM = PlayerMenu(3, 200000, 0)
        self.GhostsBots = []
        # вернуть позицию игрока.
        for i in range(self.wight):
            self.UnbrackWalls.append([])
            for j in range(self.height):
                # Генерировать не рушимиых стен.
                if ((i == 0) or (i == self.wight - 1) or (j == 0) or (j == self.height - 1)) or (
                        (i % 2 == 0) and (j % 2 == 0)):
                    self.UnbrackWalls[i].append(UnBreakWall(self.x + i * self.size, self.y + j * self.size))
        self.work = True
        self.end = False
        # Сгенерировать Рандомную позицию для Рушимых Блоков
        BWcount_tmp, GhostsBotscount_tmp = 1, 0
        while BWcount_tmp < self.BWcount:
            ist_on_anther_pint = True
            x, y = randrange(1, self.wight - 1), randrange(1, self.height - 1)
            for i in range(len(self.BrackWalls)):
                if ((self.x + x * self.size == self.BrackWalls[i].rect.x) and (
                        self.y + y * self.size == self.BrackWalls[i].rect.y)):
                    ist_on_anther_pint = False
            if (not ((x % 2 == 0) and (y % 2 == 0))) \
                and ((y * self.size != self.Player.rect.y) and ((y + 1) * self.size != self.Player.rect.y) and ((y - 1) * self.size != self.Player.rect.y)
                and (x * self.size != self.Player.rect.x) and ((x + 1) * self.size != self.Player.rect.x) and (
                (x - 1) * self.size != self.Player.rect.x)) and ist_on_anther_pint:
                if BWcount_tmp == self.BWcount // 2: self.Door = Door(self.x + x * self.size, self.y + y * self.size)
                self.BrackWalls.append(BreakWall(self.x + x * self.size, self.y + y * self.size))
                BWcount_tmp += 1

        while GhostsBotscount_tmp < self.GhostsBotscount:
            ist_on_anther_pint = True
            x, y = randrange(1, self.wight - 1), randrange(1, self.height - 1)
            for i in range(len(self.GhostsBots)):
                if ((self.x + x * self.size == self.GhostsBots[i].rect.x) and (
                        self.y + y * self.size == self.GhostsBots[i].rect.y)):
                    ist_on_anther_pint = False
            for i in range(len(self.BrackWalls)):
                if ((self.x + x * self.size == self.BrackWalls[i].rect.x) and (
                        self.y + y * self.size == self.BrackWalls[i].rect.y)):
                    ist_on_anther_pint = False
            if (not ((x % 2 == 0) and (y % 2 == 0))) \
                    and ((y * self.size != self.Player.rect.y) and ((y + 1) * self.size != self.Player.rect.y) and (
                    (y - 1) * self.size != self.Player.rect.y)
                         and (x * self.size != self.Player.rect.x) and ((x + 1) * self.size != self.Player.rect.x) and (
                                 (x - 1) * self.size != self.Player.rect.x)) \
                    and ist_on_anther_pint:
                self.GhostsBots.append(GhostBot(self.x + x * self.size, self.y + y * self.size))
                GhostsBotscount_tmp += 1

    def process_draw(self, screen):
        pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(self.x, self.y, 1280, 720), 0)  # Задний фон
        self.Door.process_draw(screen)  # Дверь
        self.Fire.process_draw(screen)  # Огонь
        self.PM.process_draw(screen)  # Меню игрока
        # Не ломаемые стены
        for i in range(len(self.UnbrackWalls)):
            for j in range(len(self.UnbrackWalls[i])):
                self.UnbrackWalls[i][j].process_draw(screen)
        for i in range(len(self.BrackWalls)): self.BrackWalls[i].process_draw(screen)  # Ломаемые стены
        self.Bomb.process_draw(screen)  # Бомба
        for i in range(len(self.GhostsBots)): self.GhostsBots[i].process_draw(screen)  # Боты
        self.Player.process_draw(screen)  # Игрок

    def process_event(self, event):
        self.Player.process_event(event)  # Игрок
        self.Bomb.process_event(event, (self.x * self.size) + (self.Player.rect.x // self.size) * self.size, (self.y - self.size) + (self.Player.rect.y // self.size) * self.size) # Бомба
        self.Fire.process_event(self.Bomb.give_existing(), self.Bomb.rect.x, self.Bomb.rect.y) # Огонь
        self.PM.process_event(event)  # Меню игрока
        for i in range(len(self.GhostsBots)): self.GhostsBots[i].process_event(event)  # Боты

    def process_logic(self):
        if self.PM.lifes <= 0 or int(self.PM.timer - pygame.time.get_ticks()) <= 0:
            self.work = False
        self.Player.process_logic()
        if self.Player.bomb == True and self.Bomb.exist_of_bomb == False:
            self.Bomb.exist_of_bomb = True
            self.Bomb.animCount = 0
            self.Bomb.rect.x = (self.x * self.size) + ((self.Player.rect.x +10 ) // self.size) * self.size
            self.Bomb.rect.y = (self.y - self.size) + ((self.Player.rect.y - 3) // self.size) * self.size
        if self.Bomb.give_existing():
            self.Fire.animCount = 0
            self.Bomb.exist_of_bomb=0
            self.Fire.rect[0].x = self.Bomb.rect.x
            self.Fire.rect[0].y = self.Bomb.rect.y
            self.Fire.exist_of_fire = True
        self.Bomb.process_logic()
        self.Fire.process_logic(self.size)
        self.PM.process_logic()
        if (len(self.GhostsBots) <= 0 and self.Player.rect1.colliderect(self.Door.rect)):
            self.end = True
            self.work = False
        # колизия:
        # Player + UnbrackWalls
        for i in range(len(self.UnbrackWalls)):
            for j in range(len(self.UnbrackWalls[i])):
                if self.Player.rect.colliderect(self.UnbrackWalls[i][j].rect):
                    if self.Player.rect1.colliderect(self.UnbrackWalls[i][j].rect):
                        if self.Player.shiftx >= 0:
                            self.Player.rect1.x -= self.Player.shift
                            self.Player.rect.x -= self.Player.shift
                        if self.Player.shiftx <= 0:
                            self.Player.rect1.x += self.Player.shift
                            self.Player.rect.x += self.Player.shift
                        if self.Player.shifty >= 0:
                            self.Player.rect1.y -= self.Player.shift
                            self.Player.rect.y -= self.Player.shift
                        if self.Player.shifty <= 0:
                            self.Player.rect1.y += self.Player.shift
                            self.Player.rect.y += self.Player.shift
        # GhostBots and Main_Character
        # GhostsBots
        for k in range(len(self.GhostsBots)):
            if self.GhostsBots[k].rect.colliderect(self.Player.rect):
                self.Player = Player(5 * self.size, 5 * self.size)
                self.PM.lifes -= 1
            for i in range(len(self.UnbrackWalls)):
                for j in range(len(self.UnbrackWalls[i])):
                    if self.GhostsBots[k].rect.colliderect(self.UnbrackWalls[i][j].rect):
                        if self.GhostsBots[k].rand == 1:
                            self.GhostsBots[k].rect.x -= 2
                            self.GhostsBots[k].rand = randrange(2, 3, 4)

                for j in range(len(self.UnbrackWalls[i])):
                    if self.GhostsBots[k].rect.colliderect(self.UnbrackWalls[i][j].rect):
                        if self.GhostsBots[k].rand == 2:
                            self.GhostsBots[k].rect.x += 2
                            self.GhostsBots[k].rand = randrange(1, 3, 4)

                for j in range(len(self.UnbrackWalls[i])):
                    if self.GhostsBots[k].rect.colliderect(self.UnbrackWalls[i][j].rect):
                        if self.GhostsBots[k].rand == 3:
                            self.GhostsBots[k].rect.y -= 2
                            self.GhostsBots[k].rand = randrange(1, 2, 4)

                for j in range(len(self.UnbrackWalls[i])):
                    if self.GhostsBots[k].rect.colliderect(self.UnbrackWalls[i][j].rect):
                        if self.GhostsBots[k].rand == 4:
                            self.GhostsBots[k].rect.y += 2
                            self.GhostsBots[k].rand = randrange(1, 2, 3)
        # BrackWalls
        # BrackWalls + Ghosts
        for i in range(len(self.BrackWalls)):
            if self.Player.rect.colliderect(self.BrackWalls[i].rect):
                if self.Player.rect1.colliderect(self.BrackWalls[i].rect):
                    if self.Player.shiftx >= 0:
                        self.Player.rect1.x -= self.Player.shift
                        self.Player.rect.x -= self.Player.shift
                    if self.Player.shiftx <= 0:
                        self.Player.rect1.x += self.Player.shift
                        self.Player.rect.x += self.Player.shift
                    if self.Player.shifty >= 0:
                        self.Player.rect1.y -= self.Player.shift
                        self.Player.rect.y -= self.Player.shift
                    if self.Player.shifty <= 0:
                        self.Player.rect1.y += self.Player.shift
                        self.Player.rect.y += self.Player.shift
            for k in range(5):
                if self.BrackWalls[i].rect.colliderect(self.Fire.rect[k]):
                    self.BrackWalls[i].enable = False
                    self.BrackWalls[i].rect.x, self.BrackWalls[i].rect.y = 0, 0
        # BrackWalls + Ghosts
        for k in range(len(self.GhostsBots)):
            for i in range(len(self.BrackWalls)):
                if self.GhostsBots[k].rect.colliderect(self.BrackWalls[i].rect):
                    if self.GhostsBots[k].rand == 1:
                        self.GhostsBots[k].rect.x -= 2
                        self.GhostsBots[k].rand = randrange(2, 3, 4)
                if self.GhostsBots[k].rect.colliderect(self.BrackWalls[i].rect):
                    if self.GhostsBots[k].rand == 2:
                        self.GhostsBots[k].rect.x += 2
                        self.GhostsBots[k].rand = randrange(1, 3, 4)
                if self.GhostsBots[k].rect.colliderect(self.BrackWalls[i].rect):
                    if self.GhostsBots[k].rand == 3:
                        self.GhostsBots[k].rect.y -= 2
                        self.GhostsBots[k].rand = randrange(1, 2, 4)
                if self.GhostsBots[k].rect.colliderect(self.BrackWalls[i].rect):
                    if self.GhostsBots[k].rand == 4:
                        self.GhostsBots[k].rect.y += 2
                        self.GhostsBots[k].rand = randrange(1, 2, 3)
        # GhostsBots обновление логики
        for i in range(len(self.GhostsBots)): self.GhostsBots[i].process_logic()
        # Fire
        for i in range(5):
            # Fire+Player
            if self.Player.rect.colliderect(self.Fire.rect[i]):
                self.Player = Player(5 * self.size, 5 * self.size)
                self.PM.lifes -= 1
            # Fire+GhostsBots
            for j in range(len(self.GhostsBots)):
                if self.GhostsBots[j].rect.colliderect(self.Fire.rect[i]):
                    self.GhostsBots.pop(j)
                    self.PM.points += 1000
                    self.PM.timer += 100000
                    return 0

    def start_game(self):
        return self.work


class PlayerMenu:

    def __init__(self, lifes, timer, points):
        self.lifes = lifes
        self.timer = timer
        self.tmp_timer = timer
        self.points = points

    def process_logic(self):
        pass

    def process_draw(self, screen):
        self.tmp_timer = int(self.tmp_timer - pygame.time.get_ticks() / 1000)
        pygame.draw.rect(screen, RGBScreen.LIGHT_GRAY, pygame.Rect(0, 0, 1280, 102), 0)
        Text_ctimer = pygame.font.SysFont('Comic Sans MS', 50, True, False).render(
            str((int((self.timer - pygame.time.get_ticks()) / 1000))), True, [128, 0, 0])
        Text_points = pygame.font.SysFont('Comic Sans MS', 50, True, False).render(str(self.points), True, [128, 0, 0])
        Text_clifes = pygame.font.SysFont('Comic Sans MS', 50, True, False).render(str(self.lifes), True, [128, 0, 0])
        Text_lifes = pygame.font.SysFont('Comic Sans MS', 50, True, False).render('Lifes: ', True, [128, 0, 0])
        Text_timer = pygame.font.SysFont('Comic Sans MS', 50, True, False).render('Time: ', True, [128, 0, 0])

        # else:
        # тут должен быть конец игры
        screen.blit(Text_timer, [10, 10])
        screen.blit(Text_ctimer, [120, 10])
        screen.blit(Text_points, [380, 10])
        screen.blit(Text_clifes, [760, 10])
        screen.blit(Text_lifes, [630, 10])

    def process_event(self, event):
        pass


class Player:
    player_stand = pygame.image.load('images/player.png')
    '''
    player_walk_left = [pygame.image.load('images/animation_player/pygame_left_1.png'),
                        pygame.image.load('images/animation_player/pygame_left_2.png'),
                        pygame.image.load('images/animation_player/pygame_left_3.png'),
                        pygame.image.load('images/animation_player/pygame_left_4.png'),
                        pygame.image.load('images/animation_player/pygame_left_5.png'),
                        pygame.image.load('images/animation_player/pygame_left_6.png')]
    player_walk_right = [pygame.image.load('images/animation_player/pygame_right_1.png'),
                         pygame.image.load('images/animation_player/pygame_right_2.png'),
                         pygame.image.load('images/animation_player/pygame_right_3.png'),
                         pygame.image.load('images/animation_player/pygame_right_4.png'),
                         pygame.image.load('images/animation_player/pygame_right_5.png'),
                         pygame.image.load('images/animation_player/pygame_right_6.png')]
    '''

    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.rect = self.player_stand.get_rect()
        self.surf1 = pygame.Surface((28, 25))
        self.rect1 = pygame.Rect((x + 3, y + 23, 28, 25))
        self.rect.x = x
        self.rect.y = y
        self.hero_died = False
        self.shift = 5
        self.shiftx = 0
        self.shifty = 0
        self.left = self.right = self.top = self.down = False
        self.animCount = 0
        self.imortal = False
        self.imortalCount = 0
        self.bomb = False

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bomb = True
            if event.key == pygame.K_a:
                self.left = True
            if event.key == pygame.K_d:
                self.right = True
            if event.key == pygame.K_w:
                self.top = True
            if event.key == pygame.K_s:
                self.down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.bomb = False
            if event.key == pygame.K_a:
                self.left = False
            if event.key == pygame.K_d:
                self.right = False
            if event.key == pygame.K_w:
                self.top = False
            if event.key == pygame.K_s:
                self.down = False
        self.dop(self.left, self.right, self.top, self.down)

    def dop(self, left, right, top, down):
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
        self.rect.x += self.shiftx
        self.rect1.x += self.shiftx
        self.rect.y += self.shifty
        self.rect1.y += self.shifty
        if self.imortal:
            if self.imortalCount + 1 >= 50:
                self.imortalCount = 0
                self.imortal = False

    def process_draw(self, screen):
        if self.animCount + 1 >= 54:
            self.animCount = 0
        '''
        if self.left:
            screen.blit(self.player_walk_left[self.animCount // 9], self.rect)
            self.animCount += 1
        elif self.right:
            screen.blit(self.player_walk_right[self.animCount // 9], self.rect)
            self.animCount += 1
        else:
            '''
        screen.blit(self.player_stand, self.rect)

    def dead(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class RGBScreen:
    GREEN = [0, 255, 0]
    BLUE = [0, 0, 255]
    RED = [255, 0, 0]
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    LIGHT_GRAY = [190, 190, 190]
    YELLOW = [255, 255, 0]
    ORANGE = [227, 121, 16]
    menu_green = [41, 89, 4]

    # выдать случайный цвет
    @staticmethod
    def get_random_color():
        return [randint(0, 250), randint(0, 250), randint(0, 250)]

    # Выдать цвет по коду RGB
    @staticmethod
    def get_color(r, g, b):
        return [r, g, b]


class MainMenu:
    font = "Retro.ttf"
    bomber_logo1 = pygame.image.load('images/bomb.png')
    bomber_logo2 = pygame.image.load('images/bomb.png')
    logo1_geom = bomber_logo1.get_rect()
    logo2_geom = bomber_logo2.get_rect()
    logo1_geom.x = 50
    logo1_geom.y = 50
    logo2_geom.x = 600
    logo2_geom.y = 50

    def __init__(self, work=True):
        self.work = work
        self.selected = "start"
        self.title = self.text_format("Bomberman", self.font, 90, RGBScreen.YELLOW)
        self.bomber_logo1 = pygame.image.load('images/bomb.png')
        self.bomber_logo2 = pygame.image.load('images/bomb.png')
        self.logo1_geom = self.bomber_logo1.get_rect()
        self.logo2_geom = self.bomber_logo2.get_rect()
        self.logo1_geom.x = 290
        self.logo1_geom.y = 125
        self.logo2_geom.x = 930
        self.logo2_geom.y = 125

    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont = pygame.font.Font(textFont, textSize)
        newText = newFont.render(message, 0, textColor)
        return newText

    def process_logic(self):
        if self.work == True:
            self.title = self.text_format("Bomberman", self.font, 150, RGBScreen.YELLOW)
            if self.selected == "start":
                self.text_start = self.text_format("START", self.font, 100, RGBScreen.RED)
            else:
                self.text_start = self.text_format("START", self.font, 100, RGBScreen.ORANGE)
            if self.selected == "quit":
                self.text_quit = self.text_format("QUIT", self.font, 100, RGBScreen.RED)
            else:
                self.text_quit = self.text_format("QUIT", self.font, 100, RGBScreen.ORANGE)
            self.title_rect = self.title.get_rect()
            self.start_rect = self.text_start.get_rect()
            self.quit_rect = self.text_quit.get_rect()

    def process_event(self, event):
        if self.work == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = "start"
                elif event.key == pygame.K_DOWN:
                    self.selected = "quit"
                if event.key == pygame.K_RETURN:
                    if self.selected == "start":
                        self.work = False
                    if self.selected == "quit":
                        pygame.quit()

    def process_draw(self, screen):
        if self.work == True:
            screen.fill(RGBScreen.menu_green)
            width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
            screen.blit(self.title, (width / 2 - (self.title_rect[2] / 2), 80))
            screen.blit(self.text_start, (width / 2 - (self.start_rect[2] / 2), 300))
            screen.blit(self.text_quit, (width / 2 - (self.quit_rect[2] / 2), 420))
            screen.blit(self.bomber_logo1, self.logo1_geom)
            screen.blit(self.bomber_logo2, self.logo2_geom)

    def start_game(self):
        return self.work


class Bomb:
    sprite_bomb = pygame.image.load('images/bomb.png')
    sprite_bomb_puls = pygame.image.load('images/bomb_puls.png')
    sprite_bomb_Boom = pygame.image.load('images/bomb_end.png')

    def __init__(self, x, y):
        self.rect = self.sprite_bomb.get_rect()
        self.exist_of_bomb = False
        self.animCount = 0
        self.rect.x = x
        self.rect.y = y

    def give_existing(self):
        if self.animCount >= 75:
            self.animCount = 0
            return True


    def process_draw(self, screen):
        if self.exist_of_bomb:
            if 0 <= self.animCount <= 75:
                if (0 <= self.animCount <= 15) or (30 <= self.animCount <= 45) or (55 <= self.animCount <= 60):
                    screen.blit(self.sprite_bomb, self.rect)
                elif (65 <= self.animCount <= 75):
                    screen.blit(self.sprite_bomb_Boom, self.rect)
                else:
                    screen.blit(self.sprite_bomb_puls, self.rect)

    def process_logic(self):
        if self.exist_of_bomb:
            self.animCount += 1
            if self.animCount >= 77:
                self.exist_of_bomb = False

    # if time - self.time1 >= 2000 and self.exist_of_bomb:
    #    self.exist_of_bomb = False

    def process_event(self, event, x, y):
        pass


class Fire:
    sprite_fire = pygame.image.load('images/fireStolb.png')
    sprite_fire_legTop = pygame.image.load('images/F3.png')
    sprite_fire_legRight = pygame.image.load('images/F4.png')
    sprite_fire_legBottom = pygame.image.load('images/F1.png')
    sprite_fire_legLeft = pygame.image.load('images/F2.png')

    def __init__(self, x, y):
        self.rect = [self.sprite_fire.get_rect(), self.sprite_fire_legTop.get_rect(),
                     self.sprite_fire_legRight.get_rect(), self.sprite_fire_legBottom.get_rect(),
                     self.sprite_fire_legLeft.get_rect()]
        self.rect[0].x = x
        self.rect[0].y = y
        self.animCount = 0
        self.exist_of_fire = False

    def process_draw(self, screen):
        if self.exist_of_fire:
            screen.blit(self.sprite_fire, (self.rect[0].x, self.rect[0].y))
            screen.blit(self.sprite_fire_legRight, (self.rect[1].x, self.rect[1].y))
            screen.blit(self.sprite_fire_legBottom, (self.rect[2].x, self.rect[2].y))
            screen.blit(self.sprite_fire_legTop, (self.rect[4].x, self.rect[4].y))
            screen.blit(self.sprite_fire_legLeft, (self.rect[3].x, self.rect[0].y))

    def process_logic(self, sized):
        self.rect[1].x, self.rect[1].y = self.rect[0].x + sized, self.rect[0].y
        self.rect[2].x, self.rect[2].y = self.rect[0].x, self.rect[0].y + sized
        self.rect[3].x, self.rect[3].y = self.rect[0].x - sized, self.rect[0].y
        self.rect[4].x, self.rect[4].y = self.rect[0].x, self.rect[0].y - sized
        if self.exist_of_fire:
            self.animCount += 1
            if self.animCount >= 50:
                self.exist_of_fire = False
                self.rect[0].x = 0
                self.rect[0].y = 0

    def process_event(self, existing, x, y):
        pass


class GhostBot:
    ghost = pygame.image.load('images/ErupbCenter.png')

    def __init__(self, x, y):
        self.rect = self.ghost.get_rect()
        self.alive = True
        self.animCount = 0
        self.rect.x = x
        self.rect.y = y
        self.rand = 1

    def process_draw(self, screen):
        screen.blit(self.ghost, self.rect)

    def process_event(self, event):
        pass

    def process_logic(self):

        if self.alive:
            self.animCount += 1
            if self.animCount >= 70:
                self.animCount = 0
                self.rand = randint(1, 4)
            if self.rand == 1:
                self.rect.x += 2
            if self.rand == 2:
                self.rect.x -= 2
            if self.rand == 3:
                self.rect.y += 2
            if self.rand == 4:
                self.rect.y -= 2


class Door:
    door = pygame.image.load('images/door.png')

    def __init__(self, x, y):
        self.rect = self.door.get_rect()
        self.rect.x = x
        self.rect.y = y

    def process_draw(self, screen):
        screen.blit(self.door, self.rect)

    def process_event(self, event):
        pass

    def process_logic(self):
        pass
