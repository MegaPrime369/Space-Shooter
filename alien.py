import pygame
from settings import Settings


class Alien(pygame.sprite.Sprite):
    def __init__(self, image_path, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (80, 80)).convert_alpha()
        self.life_left = 5
        self.rect = self.image.get_rect()
        self.moving_down = False
        self.settings = Settings()
        self.velocity_x = self.settings.alien_velocity_x
        self.velocity_y = self.settings.alien_velocity_y

    def create_healthbar(self):
        """
        Creates health bar for the player.
        :return: None
        """
        WIDTH, HEIGHT = 10, 5
        self.parts = [
            pygame.Rect(0, self.rect.top - 15, WIDTH, HEIGHT) for _ in range(5)
        ]
        self.parts[2].centerx = self.rect.centerx
        self.parts[1].right = self.parts[2].left
        self.parts[0].right = self.parts[1].left
        self.parts[3].left = self.parts[2].right
        self.parts[4].left = self.parts[3].right

    def update(self):
        """
        Moves the alien on the screen
        :return: None
        """
        self.rect.centerx += self.velocity_x
        for part in self.parts:
            part.centerx += self.velocity_x
        if self.moving_down:
            self.rect.centery += self.velocity_y
            for part in self.parts:
                part.centery += self.velocity_y
            self.moving_down = False

    def show_healthbar(self):
        """
        Shows the healthbar.
        :return: None
        """
        for part in self.parts[: self.life_left]:
            pygame.draw.rect(self.screen, "green", part)
        for part in self.parts[self.life_left :]:
            pygame.draw.rect(self.screen, "red", part)
