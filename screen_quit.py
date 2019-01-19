import pygame
from screen_base import ScreenBase

class QuitScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		font = pygame.font.Font(None, 24)
		self.text_surf = font.render("Are you sure?", True, (255,255,255))
		self.text_rect = self.text_surf.get_rect()

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_y):
				self._app.on_quit()
			elif (event.key == pygame.K_n):
				self._app.screens.change_back()

	def update(self, delta_time):
		pass
		
	def render(self, surface):
		self.text_rect.center = surface.get_rect().center
		surface.blit(self.text_surf, self.text_rect)
		rect = self.text_rect.inflate(30, 30)
		pygame.draw.rect(surface, (255,255,255), rect, 2)
