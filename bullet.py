import pygame

class Bullet(pygame.sprite.Sprite):
    # определение параметров и позиции снаряда, отрисовка спрайтом
    def __init__(self, pos, speed=8):
        super().__init__()
        self.image = pygame.Surface((4, 18))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed