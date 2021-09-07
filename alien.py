import pygame
from settings import Settings


class Alien(pygame.sprite.Sprite):
    def __init__(self, image_path, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(self.image)
        self.image = pygame.transform.scale(self.image, (150, 150)).convert_alpha()
        self.rect = self.image.get_rect()
        self.settings = Settings()

    def update(self):
        """
        Moves the alien on the screen
        :return: None
        """
        self.image_rect.centery += self.settings.alien_velocity
