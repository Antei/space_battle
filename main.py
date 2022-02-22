import pygame, sys
from player import Player
import obstacle

class Game:
    def __init__(self):
        # настройка аватара игрока
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # настройка препятствий
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks 

    def run(self):
        # обновление всех групп спрайтов
        # отрисовка всех групп спрайтов
        self.player.update()

        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)

if __name__ == '__main__':
    pygame.init()  # инициализация
    screen_width = 600  # ширина окна игры
    screen_height = 600  # высота окна игры
    # параметры окна игры
    screen = pygame.display.set_mode((screen_width, screen_height)) 
    pygame.display.set_caption('space battle')  # заголовок окна игры
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)  # ограничение частоты кадров