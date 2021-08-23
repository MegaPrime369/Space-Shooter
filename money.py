import pygame

class Money:
	def __init__(self, screen, amount):
		# Screen to show the money:-
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		# Background to show the money:-
		BACKGROUND_SIZE = (100, 30)
		self.background = pygame.image.load("Game Assets/PNG/UI/buttonRed.png")
		self.background = pygame.transform.smoothscale(self.background, BACKGROUND_SIZE).convert_alpha()
		self.background_rect = self.background.get_rect()
		self.background_rect.top = self.screen_rect.top + 20
		self.background_rect.right = self.screen_rect.right - 20
		# Font:-
		self.font = pygame.font.SysFont(None, 20)
		# Amount:-
		self.amount = amount
		# Money image:-
		MONEY_SIZE = (20, 15)
		self.money = pygame.image.load("Game Assets/PNG/Power-ups/bolt_gold.png")
		self.money = pygame.transform.smoothscale(self.money, MONEY_SIZE).convert_alpha()
		self.money_rect = self.money.get_rect()
		self.money_rect.centery = self.background_rect.centery
		self.money_rect.right= self.background_rect.right - 10

	def format_amount(self):
		"""
		Formats the amount.
		:return: String
		"""
		if self.amount >= 1000:
			formated_amount = str(float(self.amount) / 1000) + 'K'
		else:
			formated_amount = str(self.amount)
		return formated_amount

	def create_amount_image(self):
		"""
		Creates amount image/
		:return: None
		"""
		formated_amount = self.format_amount()
		self.amount_image = self.font.render(formated_amount, True, (0, 0, 0))
		self.amount_rect = self.amount_image.get_rect()
		self.amount_rect.left = self.background_rect.left + 10
		self.amount_rect.centery = self.background_rect.centery

	def show_money(self):
		"""
		Shows the money available to the screen.
		:return: None
		"""
		# Showing the background:-
		self.screen.blit(self.background, self.background_rect)
		# Showing the money:-
		self.screen.blit(self.money, self.money_rect)
		self.screen.blit(self.amount_image, self.amount_rect)
