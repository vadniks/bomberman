from src.game import Game


# это запускать
def main():
    """
    Основная функция программы - запускает меню

    :return:
    """
    g = Game()
    g.main_loop()


if __name__ == '__main__':
    main()
