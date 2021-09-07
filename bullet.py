import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image_path, velocity):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.velocity = velocity

    def update(self):
        """
        Updates the bullets position.
        :return: None
        """
        self.rect.centery += self.velocity
