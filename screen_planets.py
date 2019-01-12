import pygame
from screen_base import ScreenBase

class PlanetsScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.change_screen(self._app.screens["Quit"])
			elif (event.key == pygame.K_s):
				self._app.change_screen(self._app.screens["Stars"])
			elif (event.key == pygame.K_PERIOD):
				self._app.on_next_planet()
			elif (event.key == pygame.K_p):
				if (pygame.key.get_mods() & pygame.KMOD_LSHIFT):
					self._app.on_prev_planet()
				elif (pygame.key.get_mods() & pygame.KMOD_RSHIFT):
					self._app.on_prev_planet()
				else:
					self._app.on_next_planet()
			elif (event.key == pygame.K_COMMA):
				self._app.on_prev_planet()

	def render(self, world, surface):
		s = self._app.local_player.selected_star
		rect = s.surface.get_rect()
		rect.center = surface.get_rect().center
		surface.blit(s.surface, rect)
		for p in s.planets:
			surface.blit(p.surface, (p.x, p.y))
