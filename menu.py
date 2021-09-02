import pygame
import sys
import json
import time
from settings import Settings
from ship import MenuShip
from button import Button, ImageButton
from powerup import PowerUp
from money import Money
from notification import NotificationWindow
from game import Game


class Menu:
    def __init__(self):
        # Initialising pygame modules :-
        pygame.init()
        # Importing the settings module:-
        self.settings = Settings()
        # Initialising the screen:-
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.screen_rect = self.screen.get_rect()
        # Loading the background image:-
        self.background = pygame.image.load("Game Assets/Backgrounds/purple.png")
        self.background = pygame.transform.smoothscale(
            self.background, (self.settings.screen_width, self.settings.screen_height)
        ).convert_alpha()
        # Setting the screen caption:-
        pygame.display.set_caption(self.settings.caption)
        # Setting the font:-
        self.font = pygame.font.Font("Game Assets/Bonus/bold font.ttf", 50)
        # Setting the heading:-
        self.heading = self.font.render("Space Shooter", True, (0, 0, 0))
        self.heading_rect = self.heading.get_rect()
        self.heading_rect.centerx = self.screen_rect.centerx
        self.heading_rect.centery = self.screen_rect.top + 30
        # Creating a ship's Group:
        self.ships = pygame.sprite.Group()
        # Creating a powerup's Group:-
        self.powerups = pygame.sprite.Group()
        # Adding the ships to the group:-
        self.create_ship()
        # Adding the powerups to the group:-
        self.create_powerups()
        # Setting the font:-
        self.font = pygame.font.Font("Game Assets/Bonus/thin font.ttf", 15)
        # Making the cursor invisible:-
        pygame.mouse.set_visible(False)
        # Getting the cursor image:-
        self.cursor = pygame.image.load("Game Assets/PNG/UI/cursor.png")
        # Creating buttons:-
        self.create_buttons()
        # Limiting the incrment rate of powerup when buy button is pressed:-
        self.will_increment_powerup = True
        self.powerup_increment_time = time.time()
        # Getting the money available:-
        self.amount = self.get_object_data(["Data/User Data/money.json"])[0]
        # Creating the money status object:-
        self.money_available = Money(self.screen, self.amount)
        self.money_available.format_amount()
        self.money_available.create_amount_image()
        # Notification will be shown or not:-
        self.will_show_notification = False
        message = "You dont have enough Bolts"
        self.no_money_notification = NotificationWindow(self.screen, message)
        self.no_money_notification.create_message()
        # Initialising the sounds:-
        self.sounds = {
            "button_click": pygame.mixer.Sound("Game Assets/Bonus/button_click.ogg")
        }
        # Creating the clock to set fps:-
        self.clock = pygame.time.Clock()

    def create_powerups(self):
        """
        Create Powerups
        :return: None
        """
        powerup_number = 0
        # Getting the data of the powerups:-
        data_files = [
            "Data/PowerUp Data/Paths.json",
            "Data/PowerUp Data/powers.json",
            "Data/PowerUp Data/numbers_bought.json",
        ]
        powerup_data = self.get_object_data(data_files)
        paths, powers, numbers = powerup_data[0], powerup_data[1], powerup_data[2]
        # Setting the commong price factor:-
        price_factor = 1500
        # Creating the powerup objects:-
        for path_list in paths.values():
            for path in path_list:
                powerup = PowerUp(
                    price_factor * (powerup_number + 1),
                    path,
                    (50, 50),
                    "Game Assets/PNG/UI/green_panel.png",
                    self.screen,
                    (95, 200),
                    powers[path],
                    numbers[path],
                )
                # Setting the image position:-
                powerup.image_rect.x = (
                    2 * powerup.image_rect.width
                    + 4 * powerup_number * powerup.image_rect.width
                )
                powerup.image_rect.centery = self.screen_rect.bottom - 300
                # Setting the background position:-
                powerup.background_rect.centerx = powerup.image_rect.centerx
                powerup.background_rect.centery = powerup.image_rect.centery + 40
                # Setting the specs position:-
                powerup.spec_image_rect.centerx = powerup.image_rect.centerx
                powerup.spec_image_rect.centery = powerup.image_rect.bottom + 20
                # Setting the money image position:-
                powerup.money_image_rect.left = powerup.image_rect.centerx + 10
                powerup.money_image_rect.top = powerup.image_rect.bottom + 60
                # Setting the price_position:-
                powerup.price_image_rect.right = powerup.money_image_rect.left - 4
                powerup.price_image_rect.centery = powerup.money_image_rect.centery
                # Creating the text:-
                powerup.create_divided_texts()
                # Creating the button:-
                powerup.create_buttons()
                # Creating powerup status:-
                powerup.create_status()
                self.powerups.add(powerup)
                powerup_number += 1

    @staticmethod
    def get_object_data(files):
        """
        Gets the data of the objects from the given files.
        :return: None
        """
        # Creating a list that will store the data.
        datas = []
        # Opening the files and getting the data:-
        for file in files:
            with open(file) as data_file:
                data = json.load(data_file)
                # Appending the data to datas list:-
                datas.append(data)
        # Returning the datas list:-
        return datas

    def set_ship_state(self, ship_path, ship):
        """
        Adds text to the selected ship .
        :param ship_path: String
        :param ship: Object
        :return: None
        """
        ship_data = self.get_object_data(
            ["Data/Ship Data/in_use.json", "Data/Ship Data/is_bought.json"]
        )
        selected_ship, ships_bought = ship_data[0], ship_data[1]
        # Setting the state of the ship:-
        if ship_path == selected_ship:
            ship.is_selected = True
            # Adding 'selected' text to the selected ship.
            self.add_ship_text(ship)
            # Setting the position of the selected text:-
        if ship_path in ships_bought:
            ship.is_bought = True
        if ship_path not in ships_bought:
            # Showing the price.
            self.add_ship_text(ship)

        # Adding buttons to the ships:-
        self.add_ship_button(ship_path, ship, (selected_ship, ships_bought))

    @staticmethod
    def add_ship_text(ship):
        """
        Adds 'selected' text to the ship selected and show price.
        :param ship: Object
        :return: None
        """
        ship.prep_texts()
        if ship.is_selected:
            ship.selected_text_rect.centerx = ship.image_rect.centerx
            ship.selected_text_rect.centery = ship.image_rect.bottom + 30
        if not ship.is_bought:
            ship.price_rect.centerx = ship.image_rect.centerx
            ship.price_rect.centery = ship.image_rect.bottom + 30
            # Setting the position of money(bolt) image:-
            ship.money_rect.centerx = ship.price_rect.right + 10
            ship.money_rect.y = ship.price_rect.y

    @staticmethod
    def add_ship_button(ship_path, ship, ship_info):
        """
        Adds button to the ships like buy button and select button.
        :param ship: Object
        :param ship_path: String
        :param ship_info: Tuple
        :return: None
        """
        selected_ship, ships_bought = ship_info
        if ship_path in ships_bought and ship_path not in selected_ship:
            ship.create_button("Game Assets/PNG/UI/buttonBlue.png", "Select")
            ship.button.image_rect.centerx = ship.image_rect.centerx
            ship.button.image_rect.centery = ship.image_rect.bottom + 50
            ship.button.text_image_rect.center = ship.button.image_rect.center
            ship.has_button = True

        if ship_path not in ships_bought:
            ship.create_button("Game Assets/PNG/UI/buttonBlue.png", "Buy")
            ship.button.image_rect.centerx = ship.image_rect.centerx
            ship.button.image_rect.centery = ship.image_rect.bottom + 60
            ship.button.text_image_rect.center = ship.button.image_rect.center
            ship.has_button = True

    def create_ship(self):
        """
        Creates ships.
        :return: None
        """
        ship_number = 0
        ship_color = ["blue", "green", "orange", "red"]
        for i in range(1, 4):
            for color in ship_color:
                # Getting the path of the ship image:-
                ship_path = f"Game Assets/PNG/playerShip{i}_{color}.png"
                # Making the ship.
                ship = MenuShip(
                    str((ship_number + 1) * 1000),
                    ship_path,
                    (80, 80),
                    "Game Assets/PNG/UI/red_panel.png",
                    self.screen,
                    (40, 150),
                )
                # Setting the position of the ship.
                ship.image_rect.x = (
                    ship.image_rect.width + 2 * ship_number * ship.image_rect.width
                )
                ship.image_rect.y = self.screen_rect.top + 150
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
        if (
            self.ship_right_button.button_rect.collidepoint(mouse_pos)
            and self.ships.sprites()[0].background_rect.centerx
            < self.ships.sprites()[0].background_rect.width
        ):
            # Playing the click sound:-
            self.sounds["button_click"].play()
            for ship in self.ships.sprites():
                # Moving the ship to the right:-
                ship.move_right = True

        # Checks if the button which moves the ships left has been presses:-
        if (
            self.ship_left_button.button_rect.collidepoint(mouse_pos)
            and (
                self.screen_rect.right
                - self.ships.sprites()[11].background_rect.centerx
            )
            < self.ships.sprites()[0].background_rect.width
        ):
            # Playing the click sound:-
            self.sounds["button_click"].play()
            # Moving the ship to left:-
            for ship in self.ships.sprites():
                ship.move_left = True

        # Checks if the play button has been pressed:-
        if self.play_button.image_rect.collidepoint(mouse_pos):
            # Playing the click sound:-
            self.sounds["button_click"].play()
            time.sleep(0.09)
            # Running the game
            game = Game()
            game.run_game()

    def check_mouse_click(self):
        """
        Respond to mouse clicks.
        :return: None
        """
        # Getting the position of the mouse:-
        mouse_pos = pygame.mouse.get_pos()
        # Checks if the button in the ship has been pressed:-
        for ship in self.ships.sprites():
            if ship.check_button_click(mouse_pos):
                # Playing the click sound:-
                self.sounds["button_click"].play()
                if ship.is_bought and not ship.is_selected:
                    with open("Data/Ship Data/in_use.json", "w") as selected_file:
                        json.dump(ship.image_path, selected_file)
                    self.ships.empty()
                    self.create_ship()

                if not ship.is_bought:
                    if int(ship.price) <= int(self.money_available.amount):
                        with open("Data/Ship Data/is_bought.json", "r") as bought_file:
                            bought_list = json.load(bought_file)
                            bought_list.append(ship.image_path)
                        with open("Data/Ship Data/is_bought.json", "w") as bought_file:
                            json.dump(bought_list, bought_file)
                        self.money_available.amount -= int(ship.price)
                        self.money_available.format_amount()
                        self.money_available.create_amount_image()
                        with open("Data/User Data/money.json", "w") as money_file:
                            json.dump(self.money_available.amount, money_file)

                        self.ships.empty()
                        self.create_ship()
                    else:
                        # Getting the notification for not having money:-
                        self.will_show_notification = True
                        self.no_money_notification.counter = 1

        if self.will_show_notification:
            if self.no_money_notification.check_button_click(mouse_pos):
                # Playing the click sound:-
                self.sounds["button_click"].play()
                self.will_show_notification = False

        # Checks if the button in the powerup has been pressed:-
        # Updating the will_increment_powerup after every 0.2 seconds:-
        if time.time() - self.powerup_increment_time >= 0.2:
            self.will_increment_powerup = True

        for powerup in self.powerups.sprites():
            if powerup.check_button_click(mouse_pos) and self.will_increment_powerup:
                # Playing the click sound:-
                self.sounds["button_click"].play()
                if powerup.price <= self.money_available.amount:
                    with open(
                        "Data/PowerUp Data/numbers_bought.json"
                    ) as numbers_bought:
                        bought_dict = json.load(numbers_bought)
                    bought_dict[powerup.image_path] += 1
                    with open(
                        "Data/PowerUp Data/numbers_bought.json", "w"
                    ) as numbers_bought:
                        json.dump(bought_dict, numbers_bought)
                    # Reducing the amounf of money available:-
                    self.money_available.amount -= powerup.price
                    self.money_available.format_amount()
                    self.money_available.create_amount_image()
                    # Writing the new available money to the file:-
                    with open("Data/User Data/money.json", "w") as money_file:
                        json.dump(self.money_available.amount, money_file)
                    powerup.number = bought_dict[powerup.image_path]
                    powerup.create_status()
                    self.will_increment_powerup = False
                    self.powerup_increment_time = time.time()
                else:
                    self.will_show_notification = True
                    self.no_money_notification.counter = 1

    def create_buttons(self):
        """
        Creates button for moving the images in the menu.
        :return: None
        """
        slider_button_size = (100, 30)
        arrow_size = (50, 10)
        button_path = "Game Assets/PNG/UI/buttonYellow.png"

        # Creating the button that will move the ships to left:-
        left_arrow = pygame.image.load("Game Assets/PNG/arrow.png")
        left_arrow = pygame.transform.smoothscale(left_arrow, arrow_size)
        left_arrow = pygame.transform.rotate(left_arrow, 180).convert_alpha()
        self.ship_left_button = ImageButton(
            self.screen, left_arrow, button_path, slider_button_size
        )
        self.ship_left_button.button_rect.left = self.screen_rect.left + 10
        self.ship_left_button.button_rect.top = (
            self.ships.sprites()[0].background_rect.bottom + 10
        )
        self.ship_left_button.image_rect.center = (
            self.ship_left_button.button_rect.center
        )

        # Creating the buttons that will move the the ships to the right:-
        right_arrow = pygame.image.load("Game Assets/PNG/arrow.png")
        right_arrow = pygame.transform.smoothscale(
            right_arrow, arrow_size
        ).convert_alpha()
        self.ship_right_button = ImageButton(
            self.screen, right_arrow, button_path, slider_button_size
        )
        self.ship_right_button.button_rect.right = self.screen_rect.right - 10
        self.ship_right_button.button_rect.top = self.ship_left_button.button_rect.top
        self.ship_right_button.image_rect.center = (
            self.ship_right_button.button_rect.center
        )

        # Creating the Play Button:-
        play_button_size = (120, 40)
        self.play_button = Button(
            self.settings,
            self.screen,
            "PLAY",
            play_button_size,
            "uipack_fixed/PNG/blue_button02.png",
            25,
        )
        self.play_button.image_rect.bottom = self.screen_rect.bottom - 30
        self.play_button.image_rect.centerx = self.screen_rect.centerx
        self.play_button.text_image_rect.center = self.play_button.image_rect.center

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
        # Showing the powerups:-
        for powerup in self.powerups:
            powerup.show_powerup()
        # Show fps:-
        fps_image = self.font.render(
            f"FPS :- {round(self.clock.get_fps())}", True, (0, 0, 0)
        )
        fps_rect = fps_image.get_rect()
        fps_rect.right, fps_rect.bottom = (
            self.settings.screen_width,
            self.settings.screen_height,
        )
        self.screen.blit(fps_image, fps_rect)
        # Showing the money:-
        self.money_available.show_money()
        # Drawing the buttons:-
        self.ship_left_button.draw_image_button()
        self.ship_right_button.draw_image_button()
        # Updating the ships:-
        self.ships.update()
        if self.will_show_notification:
            self.no_money_notification.show_notification()
        # Showing the play button:-
        self.play_button.draw_button()
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
