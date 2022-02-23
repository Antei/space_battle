from re import X
from tkinter import Y
import pygame, sys
from player import Player
import obstacle
from enemy import Enemy

class Game:
    def __init__(self):
        # настройка аватара игрока
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # настройка препятствий
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_poss = [i * (screen_width / self.obstacle_amount) for i in range(self.obstacle_amount)]
        self.create_many_obstacles(*self.obstacle_x_poss, x_pos= screen_width / 15, y_pos=500)

        # настройка противников
        self.enemyes = pygame.sprite.Group()
        self.enemy_setup(rows=6, cols=8)

    def create_obstacle(self, x_pos, y_pos, offset_args):
        # создание препятствия из массива shape в obstacle 
        # c заполнением блоками только элементов 'x'
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_pos + col_index * self.block_size + offset_args
                    y = y_pos + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (250, 80, 80), x, y)
                    self.blocks.add(block)

    def create_many_obstacles(self, *offset_args, x_pos, y_pos):
        # создание большого количества препятствий
        for offset_x in offset_args:
            self.create_obstacle(x_pos, y_pos, offset_x)

    def enemy_setup(self, rows, cols, x_dist=60, y_dist=50, x_offset=65, y_offset=70):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dist + x_offset
                y = row_index * y_dist + y_offset
                if row_index == 0:
                    enemy_sprite = Enemy('red', x, y)
                if 1 <= row_index <= 2:
                    enemy_sprite = Enemy('green', x, y)
                else:
                    enemy_sprite = Enemy('blue', x, y)
                self.enemyes.add(enemy_sprite)

    def run(self):
        # обновление всех групп спрайтов
        # отрисовка всех групп спрайтов
        self.player.update()

        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        self.enemyes.draw(screen)

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