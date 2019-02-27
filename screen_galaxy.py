import os
import pygame
from screen_base import ScreenBase
from button import Button
from popup import Popup

class GalaxyScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_star = None
		self.selected_fleet = None
		
		filename = os.path.join("images", "selection.png")
		self.selection_marker_surface = pygame.image.load(filename)

		filename = os.path.join("images", "ownermarker.png")
		self.owned_star_surface = pygame.image.load(filename)

		filename = os.path.join("images", "fleet.png")
		self.fleet_surface = pygame.image.load(filename)

		filename = os.path.join("images", "shipyard.png")
		self.shipyard_surface = pygame.image.load(filename)

		self.next_turn_button = Button("End Turn", self.on_next_turn_clicked)

		self.fleet_selection_popup = None

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.on_next_turn_clicked()
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
			if self.fleet_selection_popup:
				clicked_fleet = self.fleet_selection_popup.handle_click(event)
				self.fleet_selection_popup = None
				if clicked_fleet:
					self.on_fleet_clicked(clicked_fleet)
			else:
				for s in self._app.world.stars:
					if s.rect.collidepoint(event.pos):
						self.on_star_clicked(s)

				clicked_fleets = []
				for player in self._app.players + self._app.ais:
					for fleet in player.fleets:
						if fleet.rect.collidepoint(event.pos):
							clicked_fleets.append(fleet)
				if len(clicked_fleets) == 1:
					self.on_fleet_clicked(clicked_fleets[0])
				elif len(clicked_fleets) > 1:
					self.fleet_selection_popup = Popup(
						clicked_fleets,
						clicked_fleets[0].rect.center
					)

			if self.next_turn_button.rect.collidepoint(event.pos):
				self.on_next_turn_clicked()

	def update(self, delta_time):
		pass

	def render(self, surface):
		for s in self._app.world.stars:
			surface.blit(s.surface, s.rect)

			for p in s.planets:
				if p.player:
					surface.blit(self.owned_star_surface, s.rect)

				if p.shipyard_level > 0:
					rect = s.rect.copy()
					rect.midleft = s.rect.bottomright
					surface.blit(self.shipyard_surface, rect)
			
			surface.blit(s.name_surf, s.name_rect)

		for player in self._app.players + self._app.ais:
			for f in player.fleets:
				if f.destination_star:
					pygame.draw.aaline(surface, (255,255,255), f.rect.center, f.destination_star.rect.center)
				surface.blit(self.fleet_surface, f.rect)
			
		if self.selected_star:
			surface.blit(self.selection_marker_surface, self.selected_star.rect)

		if self.selected_fleet:
			surface.blit(self.selection_marker_surface, self.selected_fleet.rect)

		self.next_turn_button.rect.topright = surface.get_rect().topright
		self.next_turn_button.render(surface)

		if self.fleet_selection_popup:
			self.fleet_selection_popup.render(surface)

	def select_star(self, star):
		if self.selected_fleet:
			self.dispatch_fleet(self.selected_fleet, star)
			self.selected_fleet = None
		else:
			if self.selected_star == star:
				screen = self._app.screens.change_to("Star")
				screen.select_star(star)
			else:
				self.selected_star = star

	def select_fleet(self, fleet):
		self.selected_fleet = fleet

	def dispatch_fleet(self, fleet, star):
		# Cannot change destination while traveling
		if not fleet.star:
			return
			
		# Cancel departure
		if star == fleet.star:
			fleet.cancel_departure()
			fleet.rect.midleft = fleet.star.rect.topright
			fleet = None
			return

		fleet.set_destination_star(star)
		fleet.rect.midright = fleet.star.rect.topleft

	def on_star_clicked(self, star):
		self.select_star(star)

	def on_fleet_clicked(self, fleet):
		self.select_fleet(fleet)

	def on_next_turn_clicked(self):
		self._app.next_turn()
