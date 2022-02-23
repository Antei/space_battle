import pygame

class Bullet(pygame.sprite.Sprite):
    # определение параметров и позиции снаряда, 
    # удаления за пределами области видимости, отрисовка спрайтом
    def __init__(self, pos, screen_height, speed=8):
        super().__init__()
        self.image = pygame.Surface((4, 18))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed

        self.height_y_constraint = screen_height

    # уничтожение снарядов, если они выходят за пределы окна
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    # передача всех действий снаряда
    def update(self):
        self.rect.y -= self.speed
        self.destroy()