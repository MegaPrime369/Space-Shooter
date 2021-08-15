from ship import MenuShip
import pygame



class PowerUp(MenuShip):
	def __init__(self, price, img_path, size, background_path, screen, offset):
		super().__init__(price, img_path, size, background_path, screen, offset)

	def show_powerup(self):
		"""
		Shows the powerup to the screen.
		:return: None
		"""
		# Drawing the background:-
		self.screen.blit(self.background, self.background_rect)
		# Drawing the powerup:-
		self.screen.blit(self.image, self.image_rect)

