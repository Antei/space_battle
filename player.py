import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        # определение аватара игрока, границ и скорости движения, настроек перезарядки орудия
        super().__init__()
        self.image = pygame.image.load('space_battle\\images\\player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint  # в границы по умолчанию передаем ширину окна
        
        self.ready = True  # статус орудия
        self.gun_time = 0  # время выстрела по умолчанию
        self.gun_cooldown = 600  # кд на перезарядку, в милисекундах

        self.bullets = pygame.sprite.Group()
    
    def get_input(self):
        # считываем события нажатия клавиш на клавиатуре
        keys = pygame.key.get_pressed()
        
        # движение по A/D или по стрелкам влево/вправо
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # выстрел по пробелу и считывание системного времени для перезарядки
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_gun()
            self.ready = False  # переключение флага готовности пока перезарядка
            self.gun_time = pygame.time.get_ticks()

    def reload(self):
        # сравнение разности текущего времени и времени выстрела 
        # для переключения флага готовности
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.gun_time >= self.gun_cooldown:
                self.ready = True

    def constraint(self):
        # проверка границ для ограничения передвижения
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_gun(self):
        # выстрел из орудия
        self.bullets.add(Bullet(self.rect.center))

    def update(self):
        # передача всех действий игрока 
        # и класса Bullet
        self.get_input()
        self.constraint()
        self.reload()
        self.bullets.update()