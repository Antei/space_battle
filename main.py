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

        # настройка статистики и количества жизней
        self.lives = 3
        self.live_surface = pygame.image.load('space_battle\\images\\player.png').convert_alpha()
        self.live_surface = pygame.transform.scale(self.live_surface, (48, 21))
        self.liv_x_start_pos = screen_width - (self.live_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.SysFont('Constantia', 24)

        # настройка препятствий
        self.shape = obstacle.shape
        self.block_size = 5
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_poss = [i * (screen_width / self.obstacle_amount) for i in range(self.obstacle_amount)]
        self.create_many_obstacles(*self.obstacle_x_poss, x_pos=screen_width / 15, y_pos=screen_height - 70)

        # настройка отряда противников
        self.enemyes = pygame.sprite.Group()
        self.enemy_shoots = pygame.sprite.Group()
        self.enemy_setup(rows=6, cols=8)
        self.enemy_x_direction = 1
        self.enemy_y_direction = 1

        # настройка элитного противника
        self.elite = pygame.sprite.GroupSingle()
        self.elite_spawn_time = randint(400, 800)

        # аудио: музыка, звук выстрела, звук взрыва
        music = pygame.mixer.Sound('space_battle\\audio\\music.wav')
        music.set_volume(0.2)
        music.play(loops=-1)
        self.bullet_sound = pygame.mixer.Sound('space_battle\\audio\\shoot.wav')
        self.bullet_sound.set_volume(0.4)
        self.exp_sound = pygame.mixer.Sound('space_battle\\audio\\explosion.wav')
        self.exp_sound.set_volume(0.3)

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

    # настройка отряда врагов
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
    # и смена направления при достижении низа или верха, или препятствия
    def enemy_border_y_checker(self):
        all_enemyes = self.enemyes.sprites()
        for enemy in all_enemyes:
            if enemy.rect.bottom >= screen_height:
                self.enemy_y_direction = 1
            elif enemy.rect.top <= 100:
                self.enemy_y_direction = -1

    # настройка случайной очередности выстрелов отряда врагов, 
    # без нее будут стрелять все сразу
    def enemy_shoot(self):
        if self.enemyes.sprites():
            random_enemy = choice(self.enemyes.sprites())
            shoot_sprite = Bullet(random_enemy.rect.center, screen_height, speed=-6)
            self.enemy_shoots.add(shoot_sprite)
            self.bullet_sound.play()

    # настройка появления элитного врага
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
                enemyes_hit = pygame.sprite.spritecollide(bullet, self.enemyes, True)
                if enemyes_hit:
                    for enemy in enemyes_hit:
                        self.score += enemy.value
                    bullet.kill()
                    self.exp_sound.play()
                # коллизии элитного врага
                if pygame.sprite.spritecollide(bullet, self.elite, True):
                    bullet.kill()
                    self.score += 500

        # выстрелы врагов
        if self.enemy_shoots:
            for bullet in self.enemy_shoots:
                # коллизии препятствий
                if pygame.sprite.spritecollide(bullet, self.blocks, True):
                    bullet.kill()
                # коллизии игрока
                if pygame.sprite.spritecollide(bullet, self.player, False):
                    bullet.kill()
                    self.lives -= 1
                    self.exp_sound.play()
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # коллизии врагов, препятствий и игрока
        if self.enemyes:
            for enemy in self.enemyes:
                if pygame.sprite.spritecollide(enemy, self.blocks, True):
                    self.enemy_y_direction = 1
                if pygame.sprite.spritecollide(enemy, self.player, False):
                    pygame.quit()
                    sys.exit()

    # отображение счетчика жизней
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.liv_x_start_pos + (live * (self.live_surface.get_size()[0] + 10))
            screen.blit(self.live_surface, (x, 8))

    # отображение статистики
    def display_score(self):
        score_surface = self.font.render(f'Score: {self.score}', False, (200, 200, 200))
        score_rect = score_surface.get_rect(topleft = (10, 10))
        screen.blit(score_surface, score_rect) 

    def victory_message(self):
       if not self.enemyes.sprites():
           victory_surf = self.font.render('Congratulations!', False, (200, 200, 200))
           victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
           screen.blit(victory_surf, victory_rect)

    # запуск, отображение и обновление картинки, etc
    def run(self):
        self.player.update()        
        self.enemy_shoots.update()
        self.elite.update()
        self.enemyes.update(self.enemy_x_direction, self.enemy_y_direction)

        self.player.draw(screen)
        self.player.sprite.bullets.draw(screen)
        self.blocks.draw(screen)
        self.enemyes.draw(screen)
        self.enemy_shoots.draw(screen)
        self.elite.draw(screen)

        self.enemy_border_x_checker()
        self.enemy_border_y_checker()
        self.collision_checks()

        self.elite_timer()

        self.display_lives()
        self.display_score()
        self.victory_message()

# стилизация под старые мониторы\телевизоры
class CRT:
    def __init__(self):
        # tv.png - от автора курса, для стилизации
        self.tv = pygame.image.load('space_battle\\images\\tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))

    # симуляция линий развертки
    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            # screen в обычных случаях, но тут надо вывести на рамку tv.png 
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)

    # симуляция мерцания и затенения по краям
    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))

if __name__ == '__main__':
    pygame.init()  # инициализация
    screen_width = 600  # ширина окна игры
    screen_height = 600  # высота окна игры
    # параметры окна игры
    screen = pygame.display.set_mode((screen_width, screen_height)) 
    pygame.display.set_caption('space battle')  # заголовок окна игры
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

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
        crt.draw()  # закомментить для отключения стилизации

        pygame.display.flip()
        clock.tick(60)  # ограничение частоты кадров