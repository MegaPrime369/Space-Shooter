import pygame


class Button:
    def __init__(self, screen, text, button_size, path, text_size):
        """
        Creates button.
        :param screen: pygame.Surface
        :param text: String
        :param button_size: Tuple
        :param path: String
        :param text_size: Integer
        """
        # Screen:-
        self.screen = screen
        # Button:-
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, button_size).convert_alpha()
        self.image_rect = self.image.get_rect()
        # Text:-
        self.text_size = text_size
        self.text = text
        self.font = pygame.font.Font('Game Assets/Bonus/thin font.ttf', self.text_size)
        self.text_image = self.font.render(self.text, True, (235, 58, 9))
        self.text_image_rect = self.text_image.get_rect()

    def draw_button(self):
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.text_image, self.text_image_rect)
