import pygame
from screen_base import ScreenBase

class QuitScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_y):
				self._app.on_quit()
			elif (event.key == pygame.K_n):
				self._app.change_screen_back()

	def update(self, world):
		pass
		
	def render(self, world, surface):
		font = pygame.font.Font(None, 24)
		text_surf = font.render("Are you sure?", True, (255,255,255))
		rect = text_surf.get_rect()
		rect.center = surface.get_rect().center
		surface.blit(text_surf, rect)

		rect.x -= 15
		rect.y -= 15
		rect.width += 30
		rect.height += 30
		pygame.draw.rect(surface, (255,255,255), rect, 2)
