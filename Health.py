from settings import *


class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.screen = pygame.display.get_surface()
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(self.screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(self.screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(self.screen, GREEN, (self.x, self.y, 150 * ratio, 20))