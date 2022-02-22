import pygame

class Block(pygame.sprite.Sprite):
    # определение размеров и положения блоков препятствий
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))

# массив, используемый как шаблон для заполнения блоками препятствий
shape = [
    '  xxxxxxx', 
    ' xxxxxxxxx', 
    'xxxxxxxxxxx', 
    'xxxxxxxxxxx',
    'xxxxxxxxxxx', 
    'xxx  x  xxx', 
    'xx       xx'
    ]

