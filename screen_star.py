import os
import pygame
from screen_base import ScreenBase

class StarScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.star = None
		self.selected_planet = None

		filename = os.path.join("images", "selection.png")
		self.selected_planet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "ownermarker.png")
		self.owned_planet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "fleet.png")
		self.fleet_surface = pygame.image.load(filename)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			elif (event.key == pygame.K_g):
				self._app.screens.change_to("Galaxy")
			elif (event.key == pygame.K_PERIOD):
				self.on_next_planet()
			elif (event.key == pygame.K_p):
				if (pygame.key.get_mods() & pygame.KMOD_LSHIFT):
					self.on_prev_planet()
				elif (pygame.key.get_mods() & pygame.KMOD_RSHIFT):
					self.on_prev_planet()
				else:
					self.on_next_planet()
			elif (event.key == pygame.K_COMMA):
				self.on_prev_planet()

		elif (event.type == pygame.MOUSEBUTTONUP):
			if self.star and self.centered_rect.collidepoint(event.pos):
				self.on_star_clicked()
			else:
				for p in self.star.planets:
					if p.rect.collidepoint(event.pos):
						self.on_planet_clicked(p)

	def update(self, delta_time):
		pass

	def render(self, surface):
		self.centered_rect.center = surface.get_rect().center
		surface.blit(self.centered_surface, self.centered_rect)
		
		self.name_rect.midtop = self.centered_rect.midbottom
		surface.blit(self.star.name_surf, self.name_rect)

		for p in self.star.planets:
			surface.blit(p.surface, p.rect)
			surface.blit(p.name_surf, p.name_rect)

			if self.selected_planet:
				surface.blit(self.selected_planet_surface, self.selected_planet.rect)

			if p.player:
				surface.blit(self.owned_planet_surface, p.rect)

			if p.fleets:
				rect = p.rect.copy()
				rect.midleft = p.rect.topright
				surface.blit(self.fleet_surface, rect)
				
	def select_star(self, star):
		self.star = star
		self.selected_planet = None

		self.centered_rect = star.rect.copy()
		self.centered_rect.width *= 3
		self.centered_rect.height *= 3
		self.centered_surface = pygame.transform.smoothscale(star.surface, self.centered_rect.size)

		self.name_rect = self.star.name_surf.get_rect()

	def on_star_clicked(self):
		self._app.screens.change_to("Galaxy")

	def on_planet_clicked(self, planet):
		if self.selected_planet == planet:
			screen = self._app.screens.change_to("Planet")
			screen.select_planet(planet)
		else:
			self.selected_planet = planet

	def on_next_planet(self):
		self.star = self._app.local_player.next_planet(self.selected_planet).star

	def on_prev_planet(self):
		self.star = self._app.local_player.prev_planet(self.selected_planet).star
