import pygame
import sys
from settings import Settings
from ship import MenuShip
from button import ImageButton
import json


class Menu:
    def __init__(self):
        # Initialising pygame modules :-
        pygame.init()
        # Importing the settings module:-
        self.settings = Settings()
        # Initialising the screen:-
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        # Loading the background image:-
        self.background = pygame.image.load('Game Assets/Backgrounds/purple.png')
        self.background = pygame.transform.scale(self.background, (
            self.settings.screen_width, self.settings.screen_height)).convert_alpha()
        # Setting the screen caption:-
        pygame.display.set_caption(self.settings.caption)
        # Setting the font:-
        self.font = pygame.font.Font('Game Assets/Bonus/bold font.ttf', 50)
        # Setting the heading:-
        self.heading = self.font.render('Space Shooter', True, (0, 0, 0))
        self.heading_rect = self.heading.get_rect()
        self.heading_rect.centerx = self.screen_rect.centerx
        self.heading_rect.centery = self.screen_rect.top + 30
        # Creating a ship's Group:
        self.ships = pygame.sprite.Group()
        # Adding the ships to the group:-
        self.create_ship()
        # Setting the font:-
        self.font = pygame.font.Font('Game Assets/Bonus/thin font.ttf', 15)
        # Making the cursor invisible:-
        pygame.mouse.set_visible(False)
        # Getting the cursor image:-
        self.cursor = pygame.image.load('Game Assets/PNG/UI/cursor.png')
        # Creating buttons:-
        self.create_buttons()
        # Creating the clock to set fps:-
        self.clock = pygame.time.Clock()

    @staticmethod
    def get_ship_data():
        """
        Gets the data of the ships.
        :return: None
        """
        # Getting the status of the ships from the json files:-
        # Getting the ship which is in use:-
        with open('Data/in_use.json') as in_use:
            selected_ship = json.load(in_use)
        # Getting the list of ships bought:-
        with open('Data/is_bought.json') as is_bought:
            ships_bought = json.load(is_bought)
        # Getting the list of ships available:-
        with open('Data/is_available.json') as is_available:
            ships_available = json.load(is_available)

        return selected_ship, ships_bought, ships_available

    def set_ship_state(self, ship_path, ship):
        """
        Adds text to the selected ship .
        :param ship_path: String
        :param ship: Object
        :return: None
        """
        selected_ship, ships_bought, ships_available = self.get_ship_data()
        # Setting the state of the ship:-
        if ship_path == selected_ship:
            ship.is_selected = True
            # Adding 'selected' text to the selected ship.
            self.add_ship_text(ship)
            # Setting the position of the selected text:-
        if ship_path in ships_bought:
            ship.is_bought = True
        if ship_path in ships_available:
            ship.is_available = True

        # Adding buttons to the ships:-
        self.add_ship_button(ship_path, ship, (selected_ship, ships_bought, ships_available))

    @staticmethod
    def add_ship_text(ship):
        """
        Adds 'selected' text to the ship selected.
        :param ship: Object
        :return: None
        """
        ship.prep_texts()
        ship.selected_text_rect.centerx = ship.image_rect.centerx
        ship.selected_text_rect.centery = ship.image_rect.bottom + 30

    @staticmethod
    def add_ship_button(ship_path, ship, ship_info):
        """
        Adds button to the ships like buy button and select button.
        :param ship: Object
        :param ship_path: String
        :param ship_info: Tuple
        :return: None
        """
        selected_ship, ships_bought, ships_available = ship_info
        if ship_path in ships_bought and ship_path not in selected_ship:
            ship.create_button('Game Assets/PNG/UI/buttonBlue.png', 'Select')
            ship.button.image_rect.centerx = ship.image_rect.centerx
            ship.button.image_rect.centery = ship.image_rect.bottom + 30
            ship.button.text_image_rect.center = ship.button.image_rect.center
            ship.has_button = True

        if ship_path not in ships_bought:
            ship.create_button('Game Assets/PNG/UI/buttonBlue.png', 'Buy')
            ship.button.image_rect.centerx = ship.image_rect.centerx
            ship.button.image_rect.centery = ship.image_rect.bottom + 30
            ship.button.text_image_rect.center = ship.button.image_rect.center
            ship.has_button = True

    def create_ship(self):
        """
        Creates ships.
        :return: None
        """
        ship_number = 0
        ship_color = ['blue', 'green', 'orange', 'red']
        for i in range(1, 4):
            for color in ship_color:
                # Getting the path of the ship image:-
                ship_path = f'Game Assets/PNG/playerShip{i}_{color}.png'
                # Making the ship.
                ship = MenuShip(ship_path, (80, 80), 'Game Assets/PNG/UI/buttonRed.png', self.screen)
                # Setting the position of the ship.
                ship.image_rect.x = ship.image_rect.width + 2 * ship_number * ship.image_rect.width
                ship.image_rect.y = self.screen_rect.top + 120
                # Setting the position of the background:-
                ship.background_rect.centerx = ship.image_rect.centerx
                ship.background_rect.centery = ship.image_rect.centery + 20
                self.set_ship_state(ship_path, ship)
                self.ships.add(ship)
                ship_number += 1

    def check_button_press(self):
        """
        Checks if the buttons in the menu has been pressed.
        :return: None
        """
        # mouse_pos:-
        mouse_pos = pygame.mouse.get_pos()
        # Checks if the button which moves the ships right has been pressed:-
        if self.ship_right_button.button_rect.collidepoint(mouse_pos) and self.ships.sprites()[
            0].background_rect.centerx < self.ships.sprites()[0].background_rect.width:
            for ship in self.ships.sprites():
                ship.move_right = True
        # Checks if the button which moves the ships left has been presses:-
        if self.ship_left_button.button_rect.collidepoint(mouse_pos) and (
                self.screen_rect.right - self.ships.sprites()[11].background_rect.centerx) < self.ships.sprites()[
            0].background_rect.width:
            for ship in self.ships.sprites():
                ship.move_left = True

    def check_mouse_click(self):
        """
        Respond to mouse clicks.
        :return: None
        """
        for ship in self.ships.sprites():
            if ship.check_button_click(pygame.mouse.get_pos()):
                if ship.is_bought and not ship.is_selected:
                    with open('Data/in_use.json', 'w') as selected_file:
                        json.dump(ship.image_path, selected_file)
                    self.ships.empty()
                    self.create_ship()

                if not ship.is_bought:
                    with open('Data/is_bought.json', 'r') as bought_file:
                        bought_list = json.load(bought_file)
                        bought_list.append(ship.image_path)
                    with open('Data/is_bought.json', 'w') as bought_file:
                        json.dump(bought_list, bought_file)
                    self.ships.empty()
                    self.create_ship()

    def create_buttons(self):
        """
        Creates button for moving the images in the menu.
        :return: None
        """
        button_size = (100, 30)
        arrow_size = (50, 10)
        button_path = 'Game Assets/PNG/UI/buttonYellow.png'
        # Creating the button that will move the ships to left:-
        left_arrow = pygame.image.load('Game Assets/PNG/arrow.png')
        left_arrow = pygame.transform.scale(left_arrow, arrow_size)
        left_arrow = pygame.transform.rotate(left_arrow, 180).convert_alpha()
        self.ship_left_button = ImageButton(self.screen, left_arrow, button_path, button_size)
        self.ship_left_button.button_rect.left = self.screen_rect.left + 10
        self.ship_left_button.button_rect.top = self.ships.sprites()[0].background_rect.bottom + 10
        self.ship_left_button.image_rect.center = self.ship_left_button.button_rect.center
        # Creating the buttons that will move the the ships to the right:-
        right_arrow = pygame.image.load('Game Assets/PNG/arrow.png')
        right_arrow = pygame.transform.smoothscale(right_arrow, arrow_size).convert_alpha()
        self.ship_right_button = ImageButton(self.screen, right_arrow, button_path, button_size)
        self.ship_right_button.button_rect.right = self.screen_rect.right - 10
        self.ship_right_button.button_rect.top = self.ship_left_button.button_rect.top
        self.ship_right_button.image_rect.center = self.ship_right_button.button_rect.center

    def check_events(self):
        """
        Checks for key presses and mouse clicks.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.check_mouse_click()
                self.check_button_press()

    def update_screen(self):
        """
        Updates screen and other objects:-
        :return: None
        """
        # Displaying the background:-
        self.screen.blit(self.background, (0, 0))
        # Show the heading:-
        self.screen.blit(self.heading, self.heading_rect)
        # Showing the ships:-
        for ship_number in range(len(self.ships)):
            var = self.ships.sprites()[ship_number]
            var.draw_ships()
        # Show fps:-
        fps_image = self.font.render(f'FPS :- {round(self.clock.get_fps())}', True, (0, 0, 0))
        fps_rect = fps_image.get_rect()
        fps_rect.right, fps_rect.bottom = self.settings.screen_width, self.settings.screen_height
        self.screen.blit(fps_image, fps_rect)
        # Drawing the buttons:-
        self.ship_left_button.draw_image_button()
        self.ship_right_button.draw_image_button()
        # Updating the ships:-
        self.ships.update()
        # Showing the cursor:-
        self.screen.blit(self.cursor, pygame.mouse.get_pos())
        # Updating the display:-
        pygame.display.flip()

    def run_menu(self):
        """
        Runs the menu window and control other functionalities.
        :return: None
        """

        # Running the game loop:-
        while True:
            # Checking for the events.
            self.check_events()
            self.update_screen()
            # Controlling the fps.
            self.clock.tick(self.settings.fps)
