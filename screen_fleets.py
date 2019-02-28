import os
import pygame
from screen_base import ScreenBase
from button import Button
from popup import Popup
from text_renderer import TextRenderer
from tile_renderer import TileRenderer

class NewFleet:
	def __init__(self):
		self.name = "New Fleet"
		self.ships = []

	def get_ship_counts(self):
		counts = {
			"Scout" : 0,
			"Frigate" : 0,
			"Destroyer" : 0,
			"Colony" : 0,
			"Total" : 0
		}
		for ship in self.ships:
			counts[ship.type] += 1
			counts["Total"] += 1

		return counts


class FleetsScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)

		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 16)
		self.text_renderer = TextRenderer(font)
		self.tile_renderer = TileRenderer(self.text_renderer)

		filename = os.path.join("images", "fleet.png")
		self.fleet_surface = pygame.image.load(filename)

		screen_rect = self._app._surface.get_rect()

		self.buttons = []

		b = Button("< 1", self.on_left_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(-32, -32)
		self.buttons.append(b)

		b = Button("< 10", self.on_left_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(-32, 0)
		self.buttons.append(b)

		b = Button("< 100", self.on_left_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(-32, 32)
		self.buttons.append(b)

		b = Button("100 >", self.on_right_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(32, -32)
		self.buttons.append(b)
	
		b = Button("10 >", self.on_right_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(32, 0)
		self.buttons.append(b)
	
		b = Button("1 >", self.on_right_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(32, 32)
		self.buttons.append(b)
	
		b = Button("Cancel", self.on_cancel_clicked)
		b.rect.bottomright = screen_rect.bottomright
		prev_button_rect = b.rect
		self.buttons.append(b)

		b = Button("Apply", self.on_apply_clicked)
		b.rect.midright = prev_button_rect.midleft
		b.rect.move_ip(-16, 0)
		prev_button_rect = b.rect
		self.buttons.append(b)

		b = Button("OK", self.on_ok_clicked)
		b.rect.midright = prev_button_rect.midleft
		b.rect.move_ip(-16, 0)
		self.buttons.append(b)

		self.fleet_selection_popup = None

	def setup(self, prev_screen_name, fleet_left):
		self.prev_screen_name = prev_screen_name
		self.new_fleet = NewFleet()
		self.fleet_left = fleet_left
		self.fleet_right = self.new_fleet
		self.popup_left = None
		self.popup_right = None
		self.ship_type_left = None
		self.ship_type_right = None

		# Fleets at the same location
		self.fleets = []
		for f in fleet_left.player.fleets:
			if f.star == fleet_left.star and f.planet == fleet_left.planet:
				self.fleets.append(f)

		screen_rect = self._app._surface.get_rect()

		self.list_left, self.list_left_rect = self.make_list(
			self.fleet_left,
			self.ship_type_left
		)
		self.list_left_rect.center = screen_rect.center
		self.list_left_rect.move_ip(-160, 0)

		self.list_right, self.list_right_rect = self.make_list(
			self.fleet_right,
			self.ship_type_right
		)
		self.list_right_rect.center = screen_rect.center
		self.list_right_rect.move_ip(160, 0)

		self.header_left = self.tile_renderer.render(
			self.fleet_left.name,
			(255,255,255),
			(64,64,64)
		)
		self.header_left_rect = self.header_left.get_rect()
		self.header_left_rect.midbottom = self.list_left_rect.midtop

		self.header_right = self.tile_renderer.render(
			self.fleet_right.name,
			(255,255,255),
			(64,64,64)
		)
		self.header_right_rect = self.header_right.get_rect()
		self.header_right_rect.midbottom = self.list_right_rect.midtop


	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if event.key == pygame.K_ESCAPE:
				self._app.screens.change_to(self.prev_screen_name)

		elif (event.type == pygame.MOUSEBUTTONUP):
			if self.popup_left:
				clicked_fleet = self.popup_left.handle_click(event)
				self.popup_left = None
				if clicked_fleet:
					self.select_left_fleet(clicked_fleet)
			elif self.popup_right:
				clicked_fleet = self.popup_right.handle_click(event)
				self.popup_right = None
				if clicked_fleet:
					self.select_right_fleet(clicked_fleet)
			elif self.header_left_rect.collidepoint(event.pos):
				self.header_left_clicked(event.pos)
			elif self.header_right_rect.collidepoint(event.pos):
				self.header_right_clicked(event.pos)
			else:
				for button in self.buttons:
					if button.rect.collidepoint(event.pos):
						button.on_click()

	def render(self, surface):
		surface.blit(self.header_left, self.header_left_rect)
		surface.blit(self.header_right, self.header_right_rect)
		surface.blit(self.list_left, self.list_left_rect)
		surface.blit(self.list_right, self.list_right_rect)
		
		if self.popup_left:
			self.popup_left.render(surface)
		if self.popup_right:
			self.popup_right.render(surface)

		for button in self.buttons:
			button.render(surface)

	def make_list(self, fleet, highlighted_ship_type):
		counts = fleet.get_ship_counts()

		scouts = self.make_ship("Scout", counts, highlighted_ship_type)
		scouts_rect = scouts.get_rect()
		scouts_rect.move_ip(8, 8)

		frigates = self.make_ship("Frigate", counts, highlighted_ship_type)
		frigates_rect = frigates.get_rect(topleft=scouts_rect.bottomleft)
		frigates_rect.move_ip(0, 8)

		destroyers = self.make_ship("Destroyer", counts, highlighted_ship_type)
		destroyers_rect = destroyers.get_rect(topleft=frigates_rect.bottomleft)
		destroyers_rect.move_ip(0, 8)

		colony = self.make_ship("Colony", counts, highlighted_ship_type)
		colony_rect = colony.get_rect(topleft=destroyers_rect.bottomleft)
		colony_rect.move_ip(0, 8)

		width = max(0, scouts_rect.width)
		width = max(width, frigates_rect.width)
		width = max(width, destroyers_rect.width)
		width = max(width, colony_rect.width)

		height = scouts_rect.height + 8 \
				+ frigates_rect.height + 8 \
				+ destroyers_rect.height + 8 \
				+ colony_rect.height

		surface = pygame.Surface((width + 16, height + 16))
		rect = surface.get_rect()

		surface.blit(scouts, scouts_rect)
		surface.blit(frigates, frigates_rect)
		surface.blit(destroyers, destroyers_rect)
		surface.blit(colony, colony_rect)

		pygame.draw.rect(surface, (255,255,255), rect, 2)

		return surface, rect

	def make_ship(self, ship_type, counts, highlighted_ship_type):
		if ship_type == highlighted_ship_type:
			background = (64,64,64)
		else:
			background = (0,0,0)

		if ship_type == "Colony":
			ship_label = "Colony Ship"
		else:
			ship_label = ship_type

		return self.text_renderer.render(
			ship_label + "s: " + str(counts[ship_type]),
			True,
			(255,255,255),
			background
		)

	def on_left_clicked(self):
		pass

	def on_right_clicked(self):
		pass

	def on_ok_clicked(self):
		on_apply_clicked()
		on_cancel_clicked()

	def on_apply_clicked(self):
		pass

	def on_cancel_clicked(self):
		self._app.screens.change_to(self.prev_screen_name)

	def header_left_clicked(self, position):
		fleet_list = self.fleets[:]
		fleet_list.append(self.new_fleet)
		fleet_list.remove(self.fleet_right)
		if len(fleet_list) > 1:
			self.popup_left = Popup(fleet_list, position)

	def header_right_clicked(self, position):
		fleet_list = self.fleets[:]
		fleet_list.append(self.new_fleet)
		fleet_list.remove(self.fleet_left)
		if len(fleet_list) > 1:
			self.popup_right = Popup(fleet_list, position)
