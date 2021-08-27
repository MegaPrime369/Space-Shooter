import pygame


class Button:
    def __init__(self, settings, screen, text, button_size, path, text_size):
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
        self.font = pygame.font.Font("Game Assets/Bonus/thin font.ttf", self.text_size)
        self.text_image = self.font.render(self.text, True, (235, 58, 9))
        self.text_image_rect = self.text_image.get_rect()
        # Settings:-
        self.settings = settings

    def draw_button(self):
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.text_image, self.text_image_rect)

    def update_button(self, move_right):
        """
        Updates the position of the button.
        :param move_right: Boolean
        :return: None
        """
        if move_right:
            self.image_rect.x += self.settings.update_magnitude
            self.text_image_rect.x += self.settings.update_magnitude
        else:
            self.image_rect.x -= self.settings.update_magnitude
            self.text_image_rect.x -= self.settings.update_magnitude


class ImageButton:
    def __init__(self, screen, image, button_path, button_size):
        """
        Initialises Attributes for button with image.
        :param screen: pygame Surface
        :param image: pygame Surface
        :param button_path: String
        :param button_size: Tuple
        """
        # Screen:-
        self.screen = screen
        # Image attributes:-
        self.image = image
        self.image_rect = self.image.get_rect()
        # Button attributes:-
        self.button = pygame.image.load(button_path)
        self.button = pygame.transform.scale(self.button, button_size).convert_alpha()
        self.button_rect = self.button.get_rect()

    def draw_image_button(self):
        """
        Draws the button to the screen.
        :return: None
        """
        self.screen.blit(self.button, self.button_rect)
        self.screen.blit(self.image, self.image_rect)
