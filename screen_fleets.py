import os
import pygame
from screen_base import ScreenBase
from ui_button import UIButton
from ui_popup import UIPopup
from ui_list import UIList
from ui_text_renderer import UITextRenderer
from ui_tile_renderer import UITileRenderer

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
		self.text_renderer = UITextRenderer(font)
		self.tile_renderer = UITileRenderer(self.text_renderer)

		filename = os.path.join("images", "fleet.png")
		self.fleet_surface = pygame.image.load(filename)

		screen_rect = self._app._surface.get_rect()

		self.buttons = []

		b = UIButton("< 1", self.on_left_1_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(-32, -32)
		self.buttons.append(b)

		b = UIButton("< 10", self.on_left_10_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(-32, 0)
		self.buttons.append(b)

		b = UIButton("< 100", self.on_left_100_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(-32, 32)
		self.buttons.append(b)

		b = UIButton("100 >", self.on_right_100_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(32, -32)
		self.buttons.append(b)
	
		b = UIButton("10 >", self.on_right_10_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(32, 0)
		self.buttons.append(b)
	
		b = UIButton("1 >", self.on_right_1_clicked)
		b.rect.center = screen_rect.center
		b.rect.move_ip(32, 32)
		self.buttons.append(b)
	
		b = UIButton("Cancel", self.on_cancel_clicked)
		b.rect.bottomright = screen_rect.bottomright
		prev_button_rect = b.rect
		self.buttons.append(b)

		b = UIButton("Apply", self.on_apply_clicked)
		b.rect.midright = prev_button_rect.midleft
		b.rect.move_ip(-16, 0)
		prev_button_rect = b.rect
		self.buttons.append(b)

		b = UIButton("OK", self.on_ok_clicked)
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

		# Get fleets at the same location
		self.fleets = []
		for f in fleet_left.player.fleets:
			if f.star == fleet_left.star and f.planet == fleet_left.planet:
				self.fleets.append(f)

		self.header_left = None
		self.header_right = None
		self.update_left_fleet()
		self.update_right_fleet()

	def update_left_fleet(self):
		screen_rect = self._app._surface.get_rect()
		pos = screen_rect.center
		pos = (pos[0] - 160, pos[1])
		self.list_left = self.make_list(self.fleet_left, pos)

		if self.header_left:
			self.buttons.remove(self.header_left)
		
		self.header_left = UIButton(self.fleet_left.name, self.header_left_clicked)
		self.header_left.rect.midbottom = self.list_left.rect.midtop
		self.buttons.append(self.header_left)

	def update_right_fleet(self):
		screen_rect = self._app._surface.get_rect()
		pos = screen_rect.center
		pos = (pos[0] + 160, pos[1])
		self.list_right = self.make_list(self.fleet_right, pos)

		if self.header_right:
			self.buttons.remove(self.header_right)
		
		self.header_right = UIButton(self.fleet_right.name, self.header_right_clicked)
		self.header_right.rect.midbottom = self.list_right.rect.midtop
		self.buttons.append(self.header_right)

	def make_list(self, fleet, position):
		counts = fleet.get_ship_counts()
		ship_buttons = [
			"Scouts: " + str(counts["Scout"]),
			"Frigates: " + str(counts["Frigate"]),
			"Destroyers: " + str(counts["Destroyer"]),
			"Colony Ships: " + str(counts["Colony"])
		]
		return UIList(ship_buttons, center=position)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if event.key == pygame.K_ESCAPE:
				self._app.screens.change_to(self.prev_screen_name)

		elif (event.type == pygame.MOUSEBUTTONUP):
			if self.popup_left:
				clicked_fleet = self.popup_left.handle_click(event)
				self.popup_left = None
				if clicked_fleet:
					self.fleet_left = clicked_fleet
					self.update_left_fleet()
			elif self.popup_right:
				clicked_fleet = self.popup_right.handle_click(event)
				self.popup_right = None
				if clicked_fleet:
					self.fleet_right = clicked_fleet
					self.update_right_fleet()
			else:
				self.list_left.handle_click(event)
				self.list_right.handle_click(event)
				for button in self.buttons:
					if button.rect.collidepoint(event.pos):
						button.on_click()

	def render(self, surface):
		self.list_left.render(surface)
		self.list_right.render(surface)
		
		if self.popup_left:
			self.popup_left.render(surface)
		if self.popup_right:
			self.popup_right.render(surface)

		for button in self.buttons:
			button.render(surface)

	def header_left_clicked(self):
		fleet_list = self.fleets[:]
		fleet_list.append(self.new_fleet)
		fleet_list.remove(self.fleet_right)
		if len(fleet_list) > 1:
			self.popup_left = UIPopup(fleet_list, self.header_left.rect.center)

	def header_right_clicked(self):
		fleet_list = self.fleets[:]
		fleet_list.append(self.new_fleet)
		fleet_list.remove(self.fleet_left)
		if len(fleet_list) > 1:
			self.popup_right = UIPopup(fleet_list, self.header_right.rect.center)

	def on_left_1_clicked(self):
		self.move_left(1)

	def on_left_10_clicked(self):
		self.move_left(10)

	def on_left_100_clicked(self):
		self.move_left(100)

	def move_left(self, amount):
		pass

	def on_right_1_clicked(self):
		self.move_right(1)

	def on_right_10_clicked(self):
		self.move_right(10)

	def on_right_100_clicked(self):
		self.move_right(100)

	def move_right(self, amount):
		pass

	def on_ok_clicked(self):
		on_apply_clicked()
		on_cancel_clicked()

	def on_apply_clicked(self):
		pass

	def on_cancel_clicked(self):
		self._app.screens.change_to(self.prev_screen_name)

