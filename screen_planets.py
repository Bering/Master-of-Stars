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

		elif (event.type == pygame.MOUSEBUTTONUP):
			for s in self._app.world.stars:
				if s.rect.collidepoint(event.pos):
					self._app.on_select_star(s)

	def update(self):
		pass

	def render(self, surface):
		star = self._app.local_player.selected_star
		rect = star.surface.get_rect()
		rect.center = surface.get_rect().center
		surface.blit(star.surface, rect)
		
		name_rect = star.name_surf.get_rect()
		name_rect.midtop = rect.midbottom
		surface.blit(star.name_surf, name_rect)

		for p in star.planets:
			surface.blit(p.surface, p.rect)
			surface.blit(p.name_surf, p.name_rect)
