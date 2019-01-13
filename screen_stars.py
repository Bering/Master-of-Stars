import pygame
from screen_base import ScreenBase

class StarsScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.change_screen(self._app.screens["Quit"])
			elif (event.key == pygame.K_PERIOD):
				self._app.on_next_planet()
			elif (event.key == pygame.K_COMMA):
				self._app.on_prev_planet()
			elif (event.key == pygame.K_p):
				if (pygame.key.get_mods() & pygame.KMOD_LSHIFT):
					self._app.on_prev_planet()
				elif (pygame.key.get_mods() & pygame.KMOD_RSHIFT):
					self._app.on_prev_planet()
				else:
					self._app.on_next_planet()
		
		elif (event.type == pygame.MOUSEBUTTONUP):
			for s in self._app.world.stars:
				rect = s.rect.move(s.x, s.y)
				if rect.collidepoint(event.pos):
					self._app.on_select_star(s)

	def update(self):
		pass

	def render(self, surface):
		for s in self._app.world.stars:
			surface.blit(s.surface, s.rect)
			surface.blit(s.name_surf, s.name_rect)
		# TODO: draw the selection marker around the selected star
