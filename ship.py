import pygame
from pygame.sprite import Sprite
from button import Button


class Ship(Sprite):
    def __init__(self, path, size):
        super().__init__()
        self.image_path = path
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, size).convert_alpha()
        self.image_rect = self.image.get_rect()


class MenuShip(Ship):
    def __init__(self, img_path, size, background_path, screen):
        super().__init__(img_path, size)
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.scale(self.background, (size[0] + 30, size[1] + 100)).convert_alpha()
        self.background_rect = self.background.get_rect()
        self.screen = screen
        self.font = pygame.font.Font('Game Assets/Bonus/thin font.ttf', 15)
        self.is_bought = False
        self.is_selected = False
        self.has_button = False
        self.move_right = False
        self.move_left = False

    def create_button(self, path, text):
        """
        Creates a button with the text.
        :param text: String
        :param path: String
        :return: None
        """
        self.button = Button(self.screen, text, (70, 30), path, 15)

    def check_button_click(self, mouse_pos):
        """
        Checks if the mouse has been clicked on the buttons related to ship class.
        :param mouse_pos: Tuple
        :return: None
        """
        if self.has_button and self.button.image_rect.collidepoint(mouse_pos):
            return True

    def prep_texts(self):
        """
        Preparing the texts.
        :return:
        """
        self.selected_text_image = self.font.render('Selected', True, (2, 51, 184))
        self.selected_text_rect = self.selected_text_image.get_rect()

    def draw_ships(self):
        """
        Draws the ship and other things to screen to the screen.
        :return: None
        """
        # Draw the background :-
        self.screen.blit(self.background, self.background_rect)
        # Draw the ship on the background:-t
        self.screen.blit(self.image, self.image_rect)
        if self.is_selected:
            self.screen.blit(self.selected_text_image, self.selected_text_rect)
        if not self.is_selected and self.is_bought:
            self.button.draw_button()
        if not self.is_bought:
            self.button.draw_button()

    def update(self):
        """
        Updates the ship's position.
        :return: None
        """
        if self.move_left:
            self.background_rect.x -= 50
            self.image_rect.x -= 50
            if self.is_selected:
                self.selected_text_rect.x -= 50
            if not self.is_selected and self.is_bought:
                self.button.update_button(False)
            if not self.is_bought:
                self.button.update_button(False)
            self.move_left = False

        elif self.move_right:
            self.background_rect.x += 50
            self.image_rect.x += 50
            if self.is_selected:
                self.selected_text_rect.x += 50
            if not self.is_selected and self.is_bought:
                self.button.update_button(True)
            if not self.is_bought:
                self.button.update_button(True)
            self.move_right = False
