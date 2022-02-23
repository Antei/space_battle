import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = 'space_battle\\images\\enemyes\\' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))

    # определение направления движения врагов
    def update(self, direction_x, direction_y):
        self.rect.x += direction_x
        self.rect.y -= direction_y