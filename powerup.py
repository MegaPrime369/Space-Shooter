from ship import MenuShip
import pygame



class PowerUp(MenuShip):
	def __init__(self, price, img_path, size, background_path, screen, offset, spec, number):
		super().__init__(price, img_path, size, background_path, screen, offset)
		# Getting the number of the powerup bought of this type:-
		self.number = number
		# Getting the specifications image:-
		self.spec = spec
		self.spec_font = pygame.font.Font('Game Assets/Bonus/thin font.ttf', 12)
		self.text_font = pygame.font.Font('Game Assets/Bonus/thin font.ttf', 15)
		self.spec_color = (89, 12, 242)
		self.button_text_color = (255, 0, 0)
		self.spec_image = self.spec_font.render(self.spec, True, self.spec_color)
		self.spec_image_rect = self.spec_image.get_rect()
		self.text_broken = False

	def create_divided_texts(self):
		"""
		Create text images.
		:return: None
		"""
		#Checking if the spec_image width is greater than the width of the background:-
		if self.spec_image_rect.width > self.background_rect.width:
			# If yes then breaking the text_in 2 parts and making text_broken = True
			self.text_broken = True
			# 1st part:-
			self.text_1 = self.spec[:int(len(self.spec)/2 + 1)]
			self.text_1_image = self.spec_font.render(self.text_1, True, self.spec_color)
			self.text_1_rect = self.text_1_image.get_rect()
			self.text_1_rect.center = self.spec_image_rect.center
			# 2nd Part:-
			self.text_2 = self.spec[int(len(self.spec)/2 + 1):]
			self.text_2_image = self.spec_font.render(self.text_2, True, self.spec_color)
			self.text_2_rect = self.text_2_image.get_rect()
			self.text_2_rect.centerx = self.spec_image_rect.centerx
			self.text_2_rect.centery = self.spec_image_rect.bottom + 15

	def create_buttons(self):
		"""
		Creates button
		:return: None
		"""
		BUTTON_SIZE = (80, 30)
		self.button_text = self.text_font.render('Buy', True, self.button_text_color)
		self.button_image = pygame.image.load('Game Assets/PNG/UI/buttonGreen.png')
		self.button_image = pygame.transform.smoothscale(self.button_image, BUTTON_SIZE).convert_alpha()
		self.button_rect = self.button_image.get_rect()
		self.button_rect.left = self.background_rect.left + 8
		self.button_rect.centery = self.image_rect.bottom + 70
		self.button_text_rect = self.button_text.get_rect()
		self.button_text_rect.center = self.button_rect.center

	def check_button_click(self, mouse_pos):
		"""
		Checks if the button has been clicked"
		:param mouse_pos: Tuple
		:return: True
		"""
		if self.button_rect.collidepoint(mouse_pos):
			return True

	def create_status(self):
		"""
		Creates images of how many powerups are bought.
		:return: None
		"""
		# Creates the platform to show the number:-
		PLATFORM_SIZE = (50, 30)
		self.platform = pygame.image.load('Game Assets/PNG/UI/buttonGreen.png')
		self.platform = pygame.transform.smoothscale(self.platform, PLATFORM_SIZE).convert_alpha()
		self.platform_rect = self.platform.get_rect()
		self.platform_rect.right = self.background_rect.right - 5
		self.platform_rect.centery = self.image_rect.bottom + 70
		# Creating an image of the number:-
		self.number_image = self.text_font.render(str(self.number), True, self.button_text_color)
		self.number_rect = self.number_image.get_rect()
		self.number_rect.center = self.platform_rect.center


	def show_powerup(self):
		"""
		Shows the powerup to the screen.
		:return: None
		"""
		# Drawing the background:-
		self.screen.blit(self.background, self.background_rect)
		# Drawing the powerup:-
		self.screen.blit(self.image, self.image_rect)
		# Showing the specifications:-
		# Checking if the text is broken down:-
		if not self.text_broken:
			self.screen.blit(self.spec_image, self.spec_image_rect)
		else:
			self.screen.blit(self.text_1_image, self.text_1_rect)
			self.screen.blit(self.text_2_image, self.text_2_rect)
		# Showing the button:-
		self.screen.blit(self.button_image, self.button_rect)
		self.screen.blit(self.button_text, self.button_text_rect)
		# Show to number of powerup number:-
		self.screen.blit(self.platform, self.platform_rect)
		self.screen.blit(self.number_image, self.number_rect)
