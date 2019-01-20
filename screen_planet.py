import os
import pygame
from screen_base import ScreenBase

class PlanetScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.planet = None

		filename = os.path.join("images", "ownermarker.png")
		surface = pygame.image.load(filename)
		self.ownermarker_rect = surface.get_rect()
		self.ownermarker_rect.width *= 3
		self.ownermarker_rect.height *= 3
		self.ownermarker = pygame.transform.smoothscale(surface, self.ownermarker_rect.size)

		filename = os.path.join("images", "fleet.png")
		surface = pygame.image.load(filename)
		self.fleet_rect = surface.get_rect()
		self.fleet_rect.width *= 2
		self.fleet_rect.height *= 2
		self.fleet_surface = pygame.transform.smoothscale(surface, self.fleet_rect.size)

		filename = os.path.join("images", "shipyard.png")
		surface = pygame.image.load(filename)
		self.shipyard_rect = surface.get_rect()
		self.shipyard_rect.width *= 2
		self.shipyard_rect.height *= 2
		self.shipyard_surface = pygame.transform.smoothscale(surface, self.shipyard_rect.size)

		filename = os.path.join("images", "defense.png")
		surface = pygame.image.load(filename)
		self.defense_rect = surface.get_rect()
		self.defense_rect.width *= 2
		self.defense_rect.height *= 2
		self.defense_surface = pygame.transform.smoothscale(surface, self.defense_rect.size)

		self.name_font = pygame.font.Font(None, 18)
		self.info_font = pygame.font.Font(None, 24)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			elif (event.key == pygame.K_g):
				self._app.screens.change_to("Galaxy")
			elif (event.key == pygame.K_s):
				self._app.screens.change_to("Star")
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
			if self.centered_rect.collidepoint(event.pos):
				self.on_planet_clicked()

	def update(self, delta_time):
		pass

	def render(self, surface):
		self.centered_rect.center = surface.get_rect().center
		surface.blit(self.centered_surface, self.centered_rect)

		if self.planet.player:
			self.ownermarker_rect.center = surface.get_rect().center
			surface.blit(self.ownermarker, self.ownermarker_rect)

		if self.planet.fleets:
			self.fleet_rect.midleft = self.centered_rect.topright
			surface.blit(self.fleet_surface, self.fleet_rect)

		if self.planet.research.tech_levels["Shipyard"] > 0:
			self.shipyard_rect.midleft = self.centered_rect.bottomright
			surface.blit(self.shipyard_surface, self.shipyard_rect)

		if self.planet.research.tech_levels["Defense"] > 0:
			self.defense_rect.midright = self.centered_rect.bottomleft
			surface.blit(self.defense_surface, self.defense_rect)

		self.name_rect.midtop = self.centered_rect.midbottom
		surface.blit(self.name_surf, self.name_rect)

		text = "Class: " + self.planet.size + " " + self.planet.type
		cls_surf = self.info_font.render(text, True, (255, 255, 255))
		cls_rect = cls_surf.get_rect()

		text = "Population: " + str(self.planet.population)
		pop_surf = self.info_font.render(text, True, (255, 255, 255))
		pop_rect = pop_surf.get_rect()

		text = "Industry: " + str(self.planet.industry)
		ind_surf = self.info_font.render(text, True, (255, 255, 255))
		ind_rect = ind_surf.get_rect()

		text = "Science: " + str(self.planet.science)
		sci_surf = self.info_font.render(text, True, (255, 255, 255))
		sci_rect = sci_surf.get_rect()

		text = "Defense: " + str(self.planet.defense)
		def_surf = self.info_font.render(text, True, (255, 255, 255))
		def_rect = def_surf.get_rect()

		text = "Shipyard: lvl" + str(self.planet.research.tech_levels["Shipyard"])
		sy_surf = self.info_font.render(text, True, (255, 255, 255))
		sy_rect = sy_surf.get_rect()

		cls_rect.midtop = self.centered_rect.midbottom
		cls_rect.centery += 48
		pop_rect.topleft = cls_rect.bottomleft
		ind_rect.topleft = pop_rect.bottomleft
		sci_rect.topleft = ind_rect.bottomleft
		def_rect.topleft = sci_rect.bottomleft
		sy_rect.topleft = def_rect.bottomleft

		surface.blit(cls_surf, cls_rect)
		surface.blit(pop_surf, pop_rect)
		surface.blit(ind_surf, ind_rect)
		surface.blit(sci_surf, sci_rect)
		surface.blit(def_surf, def_rect)
		surface.blit(sy_surf, sy_rect)

		info_rect = cls_rect.unionall(
			[pop_rect, ind_rect, sci_rect, def_rect, sy_rect]
		)
		info_rect.inflate_ip(12, 12)
		pygame.draw.rect(surface, (255,255,255), info_rect, 2)

	def select_planet(self, planet):
		self.planet = planet

		self.centered_rect = planet.rect.copy()
		self.centered_rect.width *= 3
		self.centered_rect.height *= 3
		self.centered_surface = pygame.transform.smoothscale(planet.surface, self.centered_rect.size)

		self.name_surf = self.name_font.render(self.planet.name, True, (255,255,255))
		self.name_rect = self.name_surf.get_rect()

	def on_planet_clicked(self):
		self._app.screens.change_to("Star")

	def on_next_planet(self):
		self.select_planet(self._app.local_player.next_planet(self.selected_planet).star)

	def on_prev_planet(self):
		self.select_planet(self._app.local_player.prev_planet(self.selected_planet).star)
