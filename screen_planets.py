import os
import pygame
from screen_base import ScreenBase

class PlanetsScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.star = None
		self.selected_planet = None

		filename = os.path.join("images", "selection.png")
		self.selected_planet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "ownermarker.png")
		self.owned_planet_surface = pygame.image.load(filename)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.change_screen(self._app.screens["Quit"])
			elif (event.key == pygame.K_s):
				self._app.change_screen(self._app.screens["Stars"])
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
		
		name_rect = self.star.name_surf.get_rect()
		name_rect.midtop = self.centered_rect.midbottom
		surface.blit(self.star.name_surf, name_rect)

		for p in self.star.planets:
			surface.blit(p.surface, p.rect)
			surface.blit(p.name_surf, p.name_rect)

			if self.selected_planet:
				surface.blit(self.selected_planet_surface, self.selected_planet.rect)

			if p.player:
				surface.blit(self.owned_planet_surface, p.rect)

	def select_star(self, star):
		self.star = star
		self.centered_rect = star.rect.copy()
		self.centered_rect.width = star.rect.width * 3
		self.centered_rect.height = star.rect.height * 3
		self.centered_surface = pygame.transform.scale(star.surface, self.centered_rect.size)
		self.selected_planet = None

	def on_star_clicked(self):
		self._app.change_screen(self._app.screens["Stars"])

	def on_planet_clicked(self, planet):
		self.selected_planet = planet

	def on_next_planet(self):
		self.star = self._app.local_player.next_planet(self.selected_planet).star

	def on_prev_planet(self):
		self.star = self._app.local_player.prev_planet(self.selected_planet).star
