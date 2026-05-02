import pygame
from settings import WIDTH, HEIGHT, TOOLBAR_HEIGHT, WHITE

class Canvas:
    def __init__(self):
        self.surface = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
        self.surface.fill(WHITE)

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))

    def clear(self):
        self.surface.fill(WHITE)