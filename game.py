import pygame
from pygame.sprite import Group
import sys
import json
import random
from settings import Settings
from ship import PlayerShip
from bullet import Bullet
from alien import Alien


class Game:
    def __init__(self):
        # Initialising pygame modules:-
        pygame.init()
        # Gettting the settings:-
        self.settings = Settings()
        # Creating the game window:-
        self.game_window = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # Getting the rect of the game window:-
        self.game_window_rect = self.game_window.get_rect()
        # Loading the images of the background:-
        self.background1 = pygame.image.load("Game Assets/Backgrounds/blue.png")
        self.background2 = pygame.image.load("Game Assets/Backgrounds/blue.png")
        # Resizing the images:-
        self.background1 = pygame.transform.smoothscale(
            self.background1, (self.settings.screen_width, self.settings.screen_height)
        ).convert_alpha()
        self.background2 = pygame.transform.smoothscale(
            self.background2, (self.settings.screen_width, self.settings.screen_height)
        ).convert_alpha()
        # Getting the rect of the background images:-
        self.background1_rect = self.background1.get_rect()
        self.background2_rect = self.background2.get_rect()
        self.background2_rect.bottom = self.game_window_rect.top
        # Setting the caption of the screen:-
        pygame.display.set_caption(self.settings.caption)
        # Loading the image of the mouse:-
        self.mouse_image = pygame.image.load("Game Assets/PNG/UI/cursor.png")
        # Opeing the file containing the slected ship path:-
        with open("Data/Ship Data/in_use.json") as selected_ship:
            ship_path = json.load(selected_ship)
        # Creating the player_ship:-
        self.player = PlayerShip(
            self.game_window, ship_path, self.settings.player_ship_size
        )
        self.player.image_rect.centerx = self.game_window_rect.centerx
        self.player.image_rect.bottom = self.game_window_rect.bottom - 60
        self.player.fire_rect.top = self.player.image_rect.bottom
        self.player.fire_rect.centerx = self.player.image_rect.centerx
        self.player.create_healthbar()
        # Fonts:-
        self.fonts = {"fps": pygame.font.Font("Game Assets/Bonus/thin font.ttf", 15)}
        # Groups:-
        self.player_bullets = Group()
        self.alien_group = Group()
        # Creating the aliens:-
        self.create_aliens()
        # Initialising the clock:-
        self.clock = pygame.time.Clock()

    def show_fps(self):
        """
        Shows the fps on the screen.
        :return: None
        """
        self.fps_text = self.fonts["fps"].render(
            f"FPS:- {round(self.clock.get_fps())}", True, (255, 255, 255)
        )
        self.fps_rect = self.fps_text.get_rect()
        self.fps_rect.top = self.game_window_rect.top + 5
        self.fps_rect.left = self.game_window_rect.left + 5
        self.game_window.blit(self.fps_text, self.fps_rect)

    def background_animation(self):
        """
        Runs the background animation.
        :return: None
        """
        # Checking if the background image has reached the bottom of the screen:-
        if self.background1_rect.top >= self.game_window_rect.bottom:
            self.background1_rect.bottom = self.game_window_rect.top
        if self.background2_rect.top >= self.game_window_rect.bottom:
            self.background2_rect.bottom = self.game_window_rect.top
        # Adding a velocity to the images.
        self.background2_rect.centery += self.player.velocity
        self.background1_rect.centery += self.player.velocity

    def create_bullet(self, obj_type):
        """
        Creates bullet for the player.
        :param obj_type: String
        :retrurn: None
        """
        if obj_type == 'ship':
            if "blue" in self.player.image_path:
                bullet_path = "Game Assets/PNG/Lasers/laserBlue01.png"
            elif "red" in self.player.image_path or "orange" in self.player.image_path:
                bullet_path = "Game Assets/PNG/Lasers/laserRed01.png"
            elif "green" in self.player.image_path:
                bullet_path = "Game Assets/PNG/Lasers/laserGreen11.png"

            bullet1 = Bullet(bullet_path, -self.settings.bullet_velocity)
            bullet2 = Bullet(bullet_path, -self.settings.bullet_velocity)

            bullet1.rect.centerx = self.player.image_rect.left + 2
            bullet1.rect.bottom = self.player.image_rect.centery - 10

            bullet2.rect.centerx = self.player.image_rect.right - 2
            bullet2.rect.bottom = bullet1.rect.bottom

            self.player_bullets.add(bullet1, bullet2)

        elif obj_type == 'alien':
            pass

    def delete_bullets(self):
        """
        Deletes the bullets if they go out of screen.
        :return: None
        """
        # Deleting the bullets of the player:-
        for bullet in self.player_bullets.sprites():
            if bullet.rect.bottom <= self.game_window_rect.top:
                self.player_bullets.remove(bullet)

    def create_aliens(self):
        """
        Creates aliens.
        :return: None
        """
        # Creating a test alien to get its width and height:-
        test_alien = Alien("Game Assets/PNG/Enemies/enemyBlack1.png", self.game_window)
        # Getting info:-
        alien_width = test_alien.rect.width
        alien_height = test_alien.rect.height
        # Space in x, y:-
        space_x = self.game_window_rect.width - 2 * alien_width
        num_aliens_x = int(space_x / (2 * alien_width))
        space_y = random.randint(200, 400)
        rows_num = int(space_y / (2 * alien_height))
        # Creating alien fleets :-
        for row_number in range(rows_num):
            for alien_number in range(num_aliens_x):
                # Getting a random number, color and will_add property of the enemies:-
                number = random.randint(1, 5)
                color = random.choice(["Black", "Blue", "Green", "Red"])
                will_add = random.choice([True, False])
                # Creating the alien object and reconfiguring its position:-
                alien = Alien(
                    f"Game Assets/PNG/Enemies/enemy{color}{number}.png",
                    self.game_window,
                )
                alien.rect.x = alien_width + 2 * alien_width * alien_number
                alien.rect.y = (
                    test_alien.rect.height + 2 * test_alien.rect.height * row_number
                )
                # Creating the healthbar:-
                alien.create_healthbar()
                # Adding the alien to the group:-
                if will_add:
                    self.alien_group.add(alien)

    def check_alien_pos(self):
        """
        Checks if any alien of the group touches the sides.
        :return: True
        """
        for alien in self.alien_group:
            if alien.rect.right >= self.game_window_rect.right or alien.rect.left <= self.game_window_rect.left:
                for alien in self.alien_group:
                    alien.velocity_x *= -1
                    alien.moving_down = True

    def check_alien_bullet_collision(self):
        """
        Checks if the player's bullet collides with the alien.
        :return: None
        """
        collisions = pygame.sprite.groupcollide(self.player_bullets, self.alien_group, True, False)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    if alien.life_left == 0:
                        self.alien_group.remove(alien)
                    else:
                        alien.life_left -= 1

    def check_events(self, event):
        """
        Checking events
        :return: None
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Creating a bullet for the player:-
                self.create_bullet('ship')

            if event.key == pygame.K_RIGHT:
                # Turning the moving_right attribute of the player to True.
                self.player.moving_right = True

            if event.key == pygame.K_LEFT:
                # Turning the moving_left attribute of the player to True.
                self.player.moving_left = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                # Turning the moving_right attribute of the player to False.
                self.player.moving_right = False

            if event.key == pygame.K_LEFT:
                # Turning the moving_left attribute of the player to False.
                self.player.moving_left = False

    def update_screen(self):
        """
        Updating the screen and the objects.
        :return: None
        """
        # Showing the background_image:-
        self.game_window.blit(self.background1, self.background1_rect)
        self.game_window.blit(self.background2, self.background2_rect)
        self.background_animation()
        # Showing the player:-
        self.player.show_player()
        # Showing the bullets and updating them:-
        self.player_bullets.draw(self.game_window)
        self.player_bullets.update()
        # Moving the player:-
        self.player.move_ship()
        # Deleting unwanted bullets:-
        self.delete_bullets()
        # Showing the aliens:-
        self.alien_group.draw(self.game_window)
        # Show the alien's healthbar and move them:-
        for alien in self.alien_group.sprites():
            alien.show_healthbar()
            alien.update()
        # Checking for alien, player's bullet collisions:-
        self.check_alien_bullet_collision()
        # Changing the direction of aliens:-
        self.check_alien_pos()
        # Showing the mouse:-
        self.game_window.blit(self.mouse_image, pygame.mouse.get_pos())
        # Showing the fps:-
        self.show_fps()
        # Updating the display:-
        pygame.display.flip()

    def run_game(self):

        while True:
            for event in pygame.event.get():
                self.check_events(event)
            self.update_screen()
            self.clock.tick(self.settings.fps)
