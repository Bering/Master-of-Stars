import os
import pygame
from screen_base import ScreenBase

class GalaxyScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_star = None
		
		filename = os.path.join("images", "selection.png")
		self.selection_marker_surface = pygame.image.load(filename)

		filename = os.path.join("images", "ownermarker.png")
		self.owned_star_surface = pygame.image.load(filename)

		filename = os.path.join("images", "fleet.png")
		self.fleet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "shipyard.png")
		self.shipyard_surface = pygame.image.load(filename)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
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

			for p in s.planets:
				if p.player:
					surface.blit(self.owned_star_surface, s.rect)

				if p.fleets:
					rect = s.rect.copy()
					rect.midleft = s.rect.topright
					surface.blit(self.fleet_surface, rect)
				
				if p.shipyard_level > 0:
					rect = s.rect.copy()
					rect.midleft = s.rect.bottomright
					surface.blit(self.shipyard_surface, rect)
			
			surface.blit(s.name_surf, s.name_rect)
			
		if self.selected_star:
			surface.blit(self.selection_marker_surface, self.selected_star.rect)

	def select_star(self, star):
		if self.selected_star == star:
			screen = self._app.screens.change_to("Star")
			screen.select_star(star)
		else:
			self.selected_star = star

	def on_select_star(self, star):
		select_star(star)

	def on_next_planet(self):
		screen = self._app.screens.change_to("Star")
		screen.select_star(star)
		planet = self._app.local_player.next_planet()
		screen.select_planet(planet)

	def on_prev_planet(self):
		screen = self._app.screens.change_to("Star")
		screen.select_star(star)
		planet = self._app.local_player.prev_planet()
		screen.select_planet(planet)
