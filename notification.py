import pygame
import time
from button import Button


class NotificationWindow:
    def __init__(self, screen, message):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.window = pygame.image.load("Game Assets/PNG/UI/yellow_panel.png")
        self.window = pygame.transform.smoothscale(
            self.window,
            (int(self.screen_rect.width / 2), int(self.screen_rect.height / 4)),
        ).convert_alpha()
        self.window_rect = self.window.get_rect()
        self.window_rect.center = self.screen_rect.center
        self.font = pygame.font.Font("Game Assets/Bonus/bold font.ttf", 20)
        self.message = message
        self.message_parts = []
        self.counter = 1
        self.will_show = True
        BUTTON_SIZE = (100, 50)
        BUTTON_PATH = "Game Assets/PNG/UI/buttonGreen.png"
        self.cancel_button = Button(
            None, self.screen, "Cancel", BUTTON_SIZE, BUTTON_PATH, 15
        )
        self.cancel_button.image_rect.bottom = self.window_rect.bottom - 20
        self.cancel_button.image_rect.centerx = self.window_rect.centerx
        self.cancel_button.text_image_rect.center = self.cancel_button.image_rect.center
        self.start = time.time()

    def create_message(self):
        """
        Creates the image from the message string and sets its position.
        :return: None
        """
        for i in range(len(self.message)):
            self.message_image = self.font.render(self.message[i], True, (0, 0, 0))
            self.message_rect = self.message_image.get_rect()
            self.message_rect.centerx = self.window_rect.left + (i * 20) + 50
            self.message_rect.top = self.window_rect.top + 20
            self.message_parts.append((self.message_image, self.message_rect))

    def check_button_click(self, mouse_pos):
        """
        Checks if the cancel button has been pressed
        :param mouse_pos: Tuple
        :return: Bool
        """
        if self.cancel_button.image_rect.collidepoint(mouse_pos):
            return True

    def show_notification(self):
        """
        Shows the notification on the screem.
        :return: None
        """
        if self.will_show:
            self.screen.blit(self.window, self.window_rect)
            self.cancel_button.draw_button()
            for image, rect in self.message_parts[: self.counter]:
                self.screen.blit(image, rect)

            if self.counter < len(self.message) and time.time() - self.start >= 0.05:
                self.counter += 1
                self.start = time.time()
