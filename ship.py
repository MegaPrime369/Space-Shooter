import pygame
from pygame.sprite import Sprite
from button import Button
from settings import Settings


class PlayerShip:
    def __init__(self, screen, path, size):
        super().__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image_path = path
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.smoothscale(self.image, size).convert_alpha()
        self.image_rect = self.image.get_rect()
        self.settings = Settings()
        self.velocity = self.settings.player_velocity
        self.fire = pygame.image.load(
            "Game Assets/PNG/Effects/fire05.png"
        ).convert_alpha()
        self.fire_rect = self.fire.get_rect()
        self.moving_right = False
        self.moving_left = False

    def show_player(self):
        """
        Shows the player on the screen.
        :return: None
        """
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.fire, self.fire_rect)

    def move_ship(self):
        """
        Moves the ship left and right.
        :return: None
        """
        if self.moving_right and self.image_rect.right < self.screen_rect.right:
            self.image_rect.centerx += self.settings.player_velocity
            self.fire_rect.centerx += self.settings.player_velocity
        if self.moving_left and self.image_rect.left > self.screen_rect.left:
            self.image_rect.centerx -= self.settings.player_velocity
            self.fire_rect.centerx -= self.settings.player_velocity


class MenuShip(Sprite, PlayerShip):
    def __init__(self, price, img_path, size, background_path, screen, offset):
        PlayerShip.__init__(self, screen, img_path, size)
        Sprite.__init__(self)
        self.background = pygame.image.load(background_path)
        self.background = pygame.transform.smoothscale(
            self.background, (size[0] + offset[0], size[1] + offset[1])
        ).convert_alpha()
        self.background_rect = self.background.get_rect()
        self.money = pygame.image.load("Game Assets/PNG/Power-ups/bolt_gold.png")
        self.money = pygame.transform.smoothscale(self.money, (20, 20)).convert_alpha()
        self.money_rect = self.money.get_rect()
        self.screen = screen
        self.font = pygame.font.Font("Game Assets/Bonus/thin font.ttf", 15)
        self.is_bought = False
        self.is_selected = False
        self.has_button = False
        self.move_right = False
        self.move_left = False
        self.price = price
        self.settings = Settings()
        self.update_magnitude = self.settings.update_magnitude

    def create_button(self, path, text):
        """
        Creates a button with the text.
        :param text: String
        :param path: String
        :return: None
        """
        self.button = Button(self.settings, self.screen, text, (70, 30), path, 15)

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
        # Creating the 'selected' text image:-
        self.selected_text_image = self.font.render("Selected", True, (2, 51, 184))
        self.selected_text_rect = self.selected_text_image.get_rect()
        # Creating the price of the ship image from the text:-
        self.price_image = self.font.render(self.price, True, (0, 0, 0))
        self.price_rect = self.price_image.get_rect()

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
            # Showing the price:-
            self.screen.blit(self.price_image, self.price_rect)
            self.screen.blit(self.money, self.money_rect)

    def update(self):
        """
        Updates the ship's position.
        :return: None
        """
        if self.move_left:
            self.background_rect.x -= self.update_magnitude
            self.image_rect.x -= self.update_magnitude
            if self.is_selected:
                self.selected_text_rect.x -= self.update_magnitude
            if not self.is_selected and self.is_bought:
                self.button.update_button(False)
            if not self.is_bought:
                self.button.update_button(False)
                self.price_rect.x -= self.update_magnitude
                self.money_rect.x -= self.update_magnitude
            self.move_left = False

        elif self.move_right:
            self.background_rect.x += self.update_magnitude
            self.image_rect.x += self.update_magnitude
            if self.is_selected:
                self.selected_text_rect.x += self.update_magnitude
            if not self.is_selected and self.is_bought:
                self.button.update_button(True)
            if not self.is_bought:
                self.button.update_button(True)
                self.price_rect.x += self.update_magnitude
                self.money_rect.x += self.update_magnitude
            self.move_right = False
