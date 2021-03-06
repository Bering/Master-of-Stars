import os
import pygame
from screen_base import ScreenBase
from ui_button import UIButton
from ui_popup import UIPopup
from ui_text_renderer import UITextRenderer
from ui_tile_renderer import UITileRenderer

class StarScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.star = None
		self.selected_planet = None
		self.selected_fleet = None
		self.show_fleet_info = False

		filename = os.path.join("images", "selection.png")
		self.selection_marker_surface = pygame.image.load(filename)

		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		info_font = pygame.font.Font(filename, 16)
		text_renderer = UITextRenderer(info_font)
		self.tile_renderer = UITileRenderer(text_renderer)

		self.fleet_button = UIButton("Manage", self.on_manage_fleet_clicked)
		self.next_turn_button = UIButton("End Turn", self.on_next_turn_clicked)
		self.fleet_selection_popup = None

	def setup(self, star):
		"""Setup the screen around this star"""
		self.star = star
		self.selected_planet = None
		self.selected_fleet = None
		self.show_fleet_info = False

		self.centered_rect = star.rect.copy()
		self.centered_rect.width *= 3
		self.centered_rect.height *= 3
		self.centered_surface = pygame.transform.smoothscale(star.surface, self.centered_rect.size)

		self.name_rect = self.star.name_surf.get_rect()

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.on_next_turn_clicked()
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
			if self.fleet_selection_popup:
				clicked_fleet = self.fleet_selection_popup.handle_click(event)
				self.fleet_selection_popup = None
				if clicked_fleet:
					self.on_fleet_clicked(clicked_fleet)
			else:
				if self.centered_rect.collidepoint(event.pos):
					self.on_star_clicked()
				elif self.next_turn_button.rect.collidepoint(event.pos):
					self.on_next_turn_clicked()
				elif self.show_fleet_info \
				and self.selected_fleet.player == self._app.local_player \
				and self.fleet_button.rect.collidepoint(event.pos):
					self.on_manage_fleet_clicked()
				else:
					for p in self.star.planets:
						if p.rect.collidepoint(event.pos):
							self.on_planet_clicked(p)
							return

					clicked_fleets = []
					for f in self.star.fleets:
#						if f.player == self._app.local_player:
						if f.rect_s.collidepoint(event.pos):
							clicked_fleets.append(f)
					if len(clicked_fleets) == 1:
						self.on_fleet_clicked(clicked_fleets[0])
					elif len(clicked_fleets) > 1:
						self.fleet_selection_popup = UIPopup(
							clicked_fleets,
							clicked_fleets[0].rect_s.center
						)

	def update(self, delta_time):
		pass

	def render(self, surface):

		fleets_in_orbit_around_star = []
		for f in self.star.fleets:

			if f.destination_star or f.destination_center_star_rect:
				pygame.draw.aaline(
					surface,
					(255,255,255),
					f.rect_s.center,
					self.centered_rect.center
				)

			if f.destination_planet:
				if f.player != self._app.local_player \
				and f.destination_planet.player == self._app.local_player:
					color = (255,0,0)
				else:
					color = (255,255,255)

				pygame.draw.aaline(
					surface,
					color,
					f.rect_s.center,
					f.destination_planet.rect.center
				)

			if not f.planet:
				if f.destination_star \
				or f.destination_center_star_rect \
				or f.destination_planet:
					f.rect_s = f.rect.copy()
					f.rect_s.midright = self.centered_rect.topleft
					surface.blit(f.surface, f.rect_s)
				else:
					fleets_in_orbit_around_star.append(f)

		f1, f2, f3 = self.fleet_picker(fleets_in_orbit_around_star)
		if f1:
			f1.rect_s = f1.rect.copy()
			f1.rect_s.midleft = self.centered_rect.topright
			surface.blit(f1.surface, f1.rect_s)
		if f2:
			f2.rect_s = f2.rect.copy()
			f2.rect_s.midbottom = self.centered_rect.topright
			surface.blit(f2.surface, f2.rect_s)
		if f3:
			f3.rect_s = f3.rect.copy()
			f3.rect_s.midbottom = self.centered_rect.topleft
			f3.rect_s.move_ip(35, 0)
			surface.blit(f3.surface, f3.rect_s)

		for p in self.star.planets:
			surface.blit(p.surface, p.rect)

			if self.selected_planet:
				surface.blit(self.selection_marker_surface, self.selected_planet.rect)

			if p.player:
				surface.blit(p.player.icon_ownermarker, p.rect)

			if p.shipyard_level > 0:
				rect = p.rect.copy()
				rect.midleft = p.rect.bottomright
				surface.blit(p.player.icon_shipyard, rect)

			if p.defense > 0:
				rect = p.rect.copy()
				rect.midright = p.rect.bottomleft
				surface.blit(p.player.icon_defense, rect)
			
			if p.fleets:
				fleets_in_orbit = []
				for f in p.fleets:
					if f.destination_star \
					or f.destination_center_star_rect \
					or f.destination_planet:
						rect = f.rect.copy()
						rect.midright = p.rect.topleft
						surface.blit(f.surface, f.rect_s)
					else:
						fleets_in_orbit.append(f)

				f1, f2, f3 = self.fleet_picker(fleets_in_orbit)
				if f1:
					rect = f1.rect.copy()
					rect.midleft = p.rect.topright
					surface.blit(f1.surface, rect)
				if f2:
					rect = f2.rect.copy()
					rect.midbottom = p.rect.topright
					surface.blit(f2.surface, rect)
				if f3:
					rect = f3.rect.copy()
					rect.midbottom = p.rect.topleft
					rect.move_ip(3, 0)
					surface.blit(f3.surface, rect)

			surface.blit(p.name_surf, p.name_rect)

		self.centered_rect.center = surface.get_rect().center
		surface.blit(self.centered_surface, self.centered_rect)
		
		self.name_rect.midtop = self.centered_rect.midbottom
		surface.blit(self.star.name_surf, self.name_rect)
		
		if self.selected_fleet:
			surface.blit(self.selection_marker_surface, self.selected_fleet.rect_s)

		if self.show_fleet_info:
			fleet_info_surface = self.render_fleet_text()
			fleet_info_rect = fleet_info_surface.get_rect()
			fleet_info_rect = self.move_fleet_rect(fleet_info_rect)
			surface.blit(fleet_info_surface, fleet_info_rect)
			if self.selected_fleet.player == self._app.local_player:
				self.fleet_button.rect.midtop = fleet_info_rect.midbottom
				self.fleet_button.render(surface)

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

	def render_fleet_text(self):
		ship_counts = self.selected_fleet.get_ship_counts()
		text = ""
		text += self.selected_fleet.name + "\n"
		text += "Scout(s): " + str(ship_counts["Scout"]) + "\n"
		text += "Colony Ship(s): " + str(ship_counts["Colony"]) + "\n"
		text += "Frigate(s): " + str(ship_counts["Frigate"]) + "\n"
		text += "Destroyer(s): " + str(ship_counts["Destroyer"]) + "\n"
		text += "Total: " + str(ship_counts["Total"])

		return self.tile_renderer.render(text, (255,200,200), (0,0,0))

	def move_fleet_rect(self, fleet_info_rect):
		center_x = self.centered_rect.centerx
		center_y = self.centered_rect.centery

		if self.selected_fleet.rect_s.centerx < center_x:
			if self.selected_fleet.rect_s.centery < center_y:
				fleet_info_rect.topleft = self.selected_fleet.rect_s.bottomright
				fleet_info_rect.move_ip(8, 8)
			else:
				fleet_info_rect.bottomleft = self.selected_fleet.rect_s.topright
				fleet_info_rect.move_ip(8, -8)
		else:
			if self.selected_fleet.rect_s.centery < center_y:
				fleet_info_rect.topright = self.selected_fleet.rect_s.bottomleft
				fleet_info_rect.move_ip(-8, 8)
			else:
				fleet_info_rect.bottomright = self.selected_fleet.rect_s.topleft
				fleet_info_rect.move_ip(-8, -8)

		return fleet_info_rect

	def select_planet(self, planet):
		if self.selected_fleet \
		and self.selected_fleet.player == self._app.local_player:
			self.dispatch_fleet_to_planet(self.selected_fleet, planet)
			self.selected_fleet = None
			self.show_fleet_info = False
		else:
			if self.selected_planet == planet:
				screen = self._app.screens.change_to("Planet")
				screen.setup(planet)
			else:
				self.selected_planet = planet
				self.selected_fleet = None
				self.show_fleet_info = False

	def select_fleet(self, fleet):
		if fleet == self.selected_fleet:
			self.show_fleet_info = not self.show_fleet_info
		else:
			self.selected_fleet = fleet
			self.selected_planet = None
			if fleet.player != self._app.local_player:
				self.show_fleet_info = True

	def dispatch_fleet_to_planet(self, fleet, planet):
		# Cannot change destination while traveling
		if not fleet.star:
			return
			
		# Cancel departure
		if planet == fleet.planet:
			fleet.cancel_departure()
			fleet.rect_s.midleft = fleet.planet.rect.topright
			return

		fleet.set_destination_planet(planet)
		if fleet.planet:
			fleet.rect_s.midright = fleet.planet.rect.topleft
		else:
			fleet.rect_s.midright = self.centered_rect.topleft

	def select_star(self):
		if self.selected_fleet \
		and self.selected_fleet.player == self._app.local_player:
			self.dispatch_fleet_to_star(self.selected_fleet, self.centered_rect)
			self.selected_fleet = None
			self.show_fleet_info = False
		else:
			self._app.screens.change_to("Galaxy")

	def dispatch_fleet_to_star(self, fleet, star_rect):
		# Cannot change destination while traveling
		if not fleet.star:
			return
			
		# Cancel departure
		if not fleet.planet:
			fleet.cancel_departure()
			fleet.rect_s.midleft = star_rect.topright
			return

		fleet.set_destination_center_star(star_rect)
		fleet.rect_s.midright = fleet.planet.rect.topleft

	def on_star_clicked(self):
		self.select_star()

	def on_planet_clicked(self, planet):
		self.select_planet(planet)

	def on_fleet_clicked(self, fleet):
		self.select_fleet(fleet)

	def on_next_turn_clicked(self):
		self._app.next_turn()

	def on_manage_fleet_clicked(self):
		s = self._app.screens.change_to("Fleet")
		s.setup(self.selected_fleet, "Star", self.on_back_from_fleet_screen)

	def on_back_from_fleet_screen(self, fleet_screen):
		if fleet_screen.fleet_left == None:
			if fleet_screen.fleet_right == None:
				self.selected_fleet = None
				self.show_fleet_info = False
			else:
				self.selected_fleet = fleet_screen.fleet_right
		else:
			self.selected_fleet = fleet_screen.fleet_left
