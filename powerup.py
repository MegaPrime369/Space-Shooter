from ship import MenuShip
import pygame



class PowerUp(MenuShip):
	def __init__(self, price, img_path, size, background_path, screen, offset, spec):
		super().__init__(price, img_path, size, background_path, screen, offset)
		# Getting the specifications image:-
		self.spec = spec
		self.font = pygame.font.Font('Game Assets/Bonus/thin font.ttf', 12)
		self.spec_image = self.font.render(self.spec, True, (89, 12, 242))
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
			self.text_1_image = self.font.render(self.text_1, True, (89, 12, 242))
			self.text_1_rect = self.text_1_image.get_rect()
			self.text_1_rect.center = self.spec_image_rect.center
			# 2nd Part:-
			self.text_2 = self.spec[int(len(self.spec)/2 + 1):]
			self.text_2_image = self.font.render(self.text_2, True, (89, 12, 242))
			self.text_2_rect = self.text_2_image.get_rect()
			self.text_2_rect.centerx = self.spec_image_rect.centerx
			self.text_2_rect.centery = self.spec_image_rect.bottom + 15

	def create_buttons(self):
		"""
		Creates button
		:return: None
		"""
		self.button_text = self.font.render('Buy', True, (89, 12, 242))
		self.button_image = pygame.image.load('Game Assets/PNG/UI/buttonGreen.png')
		self.button_image = pygame.transform.scale(self.button_image, (80, 30)).convert_alpha()
		self.button_rect = self.button_image.get_rect()
		self.button_rect.left = self.background_rect.left + 10
		self.button_rect.centery = self.image_rect.bottom + 70
		self.button_text_rect = self.button_text.get_rect()
		self.button_text_rect.center = self.button_rect.center

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
