import os
import pygame
from screen_base import ScreenBase

class GalaxyScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_star = None
		
		filename = os.path.join("images", "selection.png")
		self.selected_star_surface = pygame.image.load(filename)
		self.selected_star_rect = self.selected_star_surface.get_rect()

		filename = os.path.join("images", "ownermarker.png")
		self.owned_star_surface = pygame.image.load(filename)
		self.owned_star_rect = self.owned_star_surface.get_rect()

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.change_screen("Quit")
			elif (event.key == pygame.K_PERIOD):
				self.on_next_planet()
			elif (event.key == pygame.K_COMMA):
				self.on_prev_planet()
			elif (event.key == pygame.K_p):
				if (pygame.key.get_mods() & pygame.KMOD_LSHIFT):
					self.on_prev_planet()
				elif (pygame.key.get_mods() & pygame.KMOD_RSHIFT):
					self.on_prev_planet()
				else:
					self.on_next_planet()
		
		elif (event.type == pygame.MOUSEBUTTONUP):
			for s in self._app.world.stars:
				if s.rect.collidepoint(event.pos):
					self.on_select_star(s)

	def update(self, delta_time):
		pass

	def render(self, surface):
		for s in self._app.world.stars:
			surface.blit(s.surface, s.rect)
			surface.blit(s.name_surf, s.name_rect)
		
		if self.selected_star:
			surface.blit(self.selected_star_surface, self.selected_star_rect)

	def on_select_star(self, star):
		if self.selected_star == star:
			self._app.change_screen("Star")
			self._app.screens["Star"].select_star(star)
		else:
			self.selected_star = star
			self.selected_star_rect.center = star.rect.center

	def on_next_planet(self):
		self._app.change_screen("Star")
		planet = self._app.local_player.next_planet()
		self._app.screens["Star"].select_star(star)
		self._app.screens["Star"].selected_planet = planet

	def on_prev_planet(self):
		self._app.change_screen("Star")
		planet = self._app.local_player.prev_planet()
		self._app.screens["Star"].select_star(star)
		self._app.screens["Star"].selected_planet = planet
