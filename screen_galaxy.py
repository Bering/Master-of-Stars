import os
import pygame
from screen_base import ScreenBase
from ui_button import UIButton
from ui_popup import UIPopup

class GalaxyScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_star = None
		self.selected_fleet = None
		
		filename = os.path.join("images", "selection.png")
		self.selection_marker_surface = pygame.image.load(filename)

		self.next_turn_button = UIButton("End Turn", self.on_next_turn_clicked)

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
				for fleet in self._app.local_player.fleets:
					if fleet.rect.collidepoint(event.pos):
						clicked_fleets.append(fleet)
				if len(clicked_fleets) == 1:
					self.on_fleet_clicked(clicked_fleets[0])
				elif len(clicked_fleets) > 1:
					self.fleet_selection_popup = UIPopup(
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
					surface.blit(p.player.icon_ownermarker, s.rect)

				if p.shipyard_level > 0:
					rect = s.rect.copy()
					rect.midleft = s.rect.bottomright
					surface.blit(p.player.icon_shipyard, rect)

			if s.fleets:
				rect = s.rect.copy()
				orbiting_fleets = [f for f in s.fleets if not f.destination_star]
				f1, f2, f3 = self.fleet_picker(orbiting_fleets)
				if f1:
					rect.midleft = s.rect.topright
					surface.blit(f1.surface, rect)
				if f2:
					rect.midbottom = s.rect.topright
					surface.blit(f2.surface, rect)
				if f3:
					rect.midbottom = s.rect.topleft
					rect.move_ip(3, 0)
					surface.blit(f3.surface, rect)
			
			surface.blit(s.name_surf, s.name_rect)

		for player in self._app.players + self._app.ais:
			for f in player.fleets:
				if f.destination_star:
					# TODO: red for incoming enemy fleet
					pygame.draw.aaline(
						surface,
						player.color,
						f.rect.center,
						f.destination_star.rect.center
					)
					surface.blit(f.surface, f.rect)
			
		if self.selected_star:
			surface.blit(self.selection_marker_surface, self.selected_star.rect)

		if self.selected_fleet:
			surface.blit(self.selection_marker_surface, self.selected_fleet.rect)

		self.next_turn_button.rect.topright = surface.get_rect().topright
		self.next_turn_button.rect.move_ip(-16, 16)
		self.next_turn_button.render(surface)

		if self.fleet_selection_popup:
			self.fleet_selection_popup.render(surface)

	# 3 fleets to choose
	# if local player has a fleet, it must be f1
	# only choose the first fleet of every player
	# if more than 3 players, only choose the first 3
	def fleet_picker(self, fleets):
		f1 = None
		f2 = None
		f3 = None
		player_fleets = {}

		# First fleet of every player
		for f in fleets:
			if f.player not in player_fleets:
				player_fleets[f.player] = f

		# if local player has a fleet, it is f1
		if self._app.local_player in player_fleets:
			f1 = player_fleets[self._app.local_player]
			del player_fleets[self._app.local_player]

		for player, fleet in player_fleets.items():
			if not f1:
				f1 = player_fleets[player]
			elif not f2:
				f2 = player_fleets[player]
			elif not f3:
				f3 = player_fleets[player]
			else:
				break

		return f1, f2, f3

	def select_star(self, star):
		if self.selected_fleet:
			self.dispatch_fleet(self.selected_fleet, star)
			self.selected_fleet = None
		else:
			if self.selected_star == star:
				screen = self._app.screens.change_to("Star")
				screen.setup(star)
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
