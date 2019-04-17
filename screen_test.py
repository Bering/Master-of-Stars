import pygame
from screen_base import ScreenBase

class TestScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		font = pygame.font.Font(None, 24)

		anchor = self._app._surface.get_rect().center
		for p in self._app.players + self._app.ais:
			p.test_text = font.render(
				"("+str(p.color[0])+","+str(p.color[1])+","+str(p.color[2])+")",
				True,
				p.color
			)
			p.test_rect = p.test_text.get_rect()
			p.test_rect.topleft = anchor
			anchor = p.test_rect.bottomleft

	def setup(self, prev_screen_name):
		self.prev_screen_name = prev_screen_name

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to(self.prev_screen_name)

	def render(self, surface):
		for p in self._app.players + self._app.ais:
			surface.blit(p.test_text, p.test_rect)
			frect = p.fleets[0].rect.copy()
			frect.midright = p.test_rect.midleft
			surface.blit(p.fleets[0].surface, frect)
