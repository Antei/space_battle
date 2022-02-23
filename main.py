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

        # настройка матрицы размерности отряда противников
        self.enemyes = pygame.sprite.Group()
        self.enemy_setup(rows=6, cols=8)
        self.enemy_x_direction = 1
        self.enemy_y_direction = 1

    # создание препятствия из массива shape в obstacle 
    # c заполнением блоками только элементов 'x'
    def create_obstacle(self, x_pos, y_pos, offset_args):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_pos + col_index * self.block_size + offset_args
                    y = y_pos + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (250, 80, 80), x, y)
                    self.blocks.add(block)

    # создание некоторого количества препятствий
    def create_many_obstacles(self, *offset_args, x_pos, y_pos):
        for offset_x in offset_args:
            self.create_obstacle(x_pos, y_pos, offset_x)

    # настройка отряда противников
    def enemy_setup(self, rows, cols, x_dist=60, y_dist=50, x_offset=65, y_offset=70):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dist + x_offset
                y = row_index * y_dist + y_offset
                if row_index == 0:
                    enemy_sprite = Enemy('red', x, y)
                elif 1 <= row_index <= 2:
                    enemy_sprite = Enemy('green', x, y)
                else:
                    enemy_sprite = Enemy('yellow', x, y)
                self.enemyes.add(enemy_sprite)

    # проверка границ для ограничения передвижения отряда врагов 
    # и смена направления при достижении границы по горизонтали
    def enemy_border_x_checker(self):
        all_enemyes = self.enemyes.sprites()
        for enemy in all_enemyes:
            if enemy.rect.right >= screen_width:
                self.enemy_x_direction = -1
                # self.enemy_move_down(2)  # вариант автора курса
            elif enemy.rect.left <= 0:
                self.enemy_x_direction = 1
                # self.enemy_move_down(2)  # вариант автора курса

    # проверка границ для ограничения передвижения отряда врагов 
    # и смена направления при достижении границы по вертикали
    def enemy_border_y_checker(self):
        all_enemyes = self.enemyes.sprites()
        for enemy in all_enemyes:
            if enemy.rect.bottom >= screen_height - 100:
                self.enemy_y_direction = 1
            elif enemy.rect.top <= 50:
                self.enemy_y_direction = -1

    # вариант от автора изначального курса, не используется, но пока пусть будет
#    def enemy_move_down(self, distance):
#        if self.enemyes:
#            for enemy in self.enemyes.sprites():
#                enemy.rect.y += distance

    # обновление всех групп спрайтов
    # отрисовка всех групп спрайтов    
    def run(self):
        self.player.update()
        self.enemyes.update(self.enemy_x_direction, self.enemy_y_direction)
        self.enemy_border_x_checker()
        self.enemy_border_y_checker()

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