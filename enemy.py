import pygame

class Enemy(pygame.sprite.Sprite):
    # обычные враги
    def __init__(self, color, x, y):
        super().__init__()
        file_path = 'space_battle\\images\\enemyes\\' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))

    # определение направления движения врагов
    def update(self, direction_x, direction_y):
        self.rect.x += direction_x
        self.rect.y -= direction_y

class ELite(pygame.sprite.Sprite):
    # элитный враг
    def __init__(self, side, screen_width):
        super().__init__()
        self.image = pygame.image.load('space_battle\\images\\enemyes\\elite.png').convert_alpha()
        
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3
        
        self.rect = self.image.get_rect(topleft = (x, 60))

    def update(self):
        self.rect.x += self.speed