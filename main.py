import pygame, sys
from player import Player
import obstacle
from enemy import Enemy, ELite
from bullet import Bullet
from random import choice, randint

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

        # настройка отряда противников
        self.enemyes = pygame.sprite.Group()
        self.enemy_shoots = pygame.sprite.Group()
        self.enemy_setup(rows=6, cols=8)
        self.enemy_x_direction = 1
        self.enemy_y_direction = 1

        # настройка элитного противника
        self.elite = pygame.sprite.GroupSingle()
        self.elite_spawn_time = randint(400, 800)

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
            elif enemy.rect.left <= 0:
                self.enemy_x_direction = 1

    # проверка границ для ограничения передвижения отряда врагов 
    # и смена направления при достижении границы по вертикали
    def enemy_border_y_checker(self):
        all_enemyes = self.enemyes.sprites()
        for enemy in all_enemyes:
            if enemy.rect.bottom >= screen_height:
                self.enemy_y_direction = 1
            elif enemy.rect.top <= 100:
                self.enemy_y_direction = -1

    def enemy_shoot(self):
        if self.enemyes.sprites():
            random_enemy = choice(self.enemyes.sprites())
            shoot_sprite = Bullet(random_enemy.rect.center, screen_height, speed=-6)
            self.enemy_shoots.add(shoot_sprite)

    def elite_timer(self):
        self.elite_spawn_time -= 1
        if self.elite_spawn_time <= 0:
            self.elite.add(ELite(choice(('right', 'left')), screen_width))
            self.elite_spawn_time = randint(400, 800)

    # проверка коллизий между игроком и выстрелами врагов, препятствиями, 
    # а также между выстрелами игрока и врагами
    def collision_checks(self):

        # выстрелы игрока
        if self.player.sprite.bullets:
            for bullet in self.player.sprite.bullets:
                # коллизии препятствий
                if pygame.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                # коллизии врагов
                if pygame.sprite.spritecollide(bullet, self.enemyes, True):
                    bullet.kill()
                # коллизии элитного врага
                if pygame.sprite.spritecollide(bullet, self.elite, True):
                    bullet.kill()

        # выстрелы врагов
        if self.enemy_shoots:
            for bullet in self.enemy_shoots:
                # коллизии препятствий
                if pygame.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                # коллизии игрока
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    print('dead')

        # враги
        if self.enemyes:
            for enemy in self.enemyes:
                pygame.sprite.spritecollide(enemy, self.blocks, True)
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    pygame.quit()
                    sys.exit()

    # обновление всех групп спрайтов
    # отрисовка всех групп спрайтов    
    def run(self):
        self.player.update()
        self.player.sprite.bullets.draw(screen)
        self.player.draw(screen)

        self.enemyes.update(self.enemy_x_direction, self.enemy_y_direction)
        self.enemy_border_x_checker()
        self.enemy_border_y_checker()
        self.enemy_shoots.update()
        self.elite_timer()
        self.elite.update()

        self.blocks.draw(screen)
        self.enemyes.draw(screen)
        self.enemy_shoots.draw(screen)
        self.elite.draw(screen)

        self.collision_checks()

if __name__ == '__main__':
    pygame.init()  # инициализация
    screen_width = 600  # ширина окна игры
    screen_height = 600  # высота окна игры
    # параметры окна игры
    screen = pygame.display.set_mode((screen_width, screen_height)) 
    pygame.display.set_caption('space battle')  # заголовок окна игры
    clock = pygame.time.Clock()
    game = Game()

    # событие выстрела противниками в игрока
    ENEMYSHOOT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMYSHOOT, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ENEMYSHOOT:
                game.enemy_shoot()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)  # ограничение частоты кадров