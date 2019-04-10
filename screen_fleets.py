import os
import pygame
from screen_base import ScreenBase
from fleet import Fleet
from ui_button import UIButton
from ui_popup import UIPopup
from ui_list import UIList
from ui_text_renderer import UITextRenderer
from ui_tile_renderer import UITileRenderer

# This is to append "New Fleet" at the end of fleet popups
class NewFleetOption():
	def __init__(self):
		self.name = "New Fleet"

# TODO: this requires a valid planet but I want to be able to manage fleets in orbit around stars...
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

		self.header_left = None
		self.header_right = None

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
	
		self.disband_fleet_left = UIButton("Disband", self.on_disband_fleet_left_clicked)
		self.buttons.append(self.disband_fleet_left)
	
		self.disband_fleet_right = UIButton("Disband", self.on_disband_fleet_right_clicked)
		self.buttons.append(self.disband_fleet_right)
	
		b = UIButton("OK", self.on_ok_clicked)
		b.rect.bottomright = screen_rect.bottomright
		b.rect.move_ip(-16, -16)
		self.buttons.append(b)

		self.fleet_selection_popup = None

	def setup(self, prev_screen_name, fleet_left):
		self.prev_screen_name = prev_screen_name
		self.player = fleet_left.player
		self.planet = fleet_left.planet # TODO: this requires a valid planet but I want to be able to manage fleets in orbit around stars...

		# Get fleets at the same location
		self.fleets = []
		for f in fleet_left.player.fleets:
			if f.star == fleet_left.star and f.planet == fleet_left.planet:
				self.fleets.append(f)

		self.fleet_left = fleet_left

		other_fleets = self.fleets[:]
		other_fleets.remove(fleet_left)
		if len(other_fleets) == 0:
			self.fleet_right = None
		else:
			self.fleet_right = other_fleets[0]

		self.popup_left = None
		self.popup_right = None
		self.list_left = None
		self.list_right = None

		self.update_left_list()
		self.update_right_list()

	def update_left_list(self):
		if self.list_left:
			selected_index = self.list_left.get_selected_index()
		else:
			selected_index = None

		screen_rect = self._app._surface.get_rect()
		pos = screen_rect.center
		pos = (pos[0] - 160, pos[1])
		if self.fleet_left:
			self.list_left = self.make_list(self.fleet_left, pos)

			if selected_index != None:
				self.list_left.select(selected_index)
		else:
			self.list_left = None

		if self.header_left:
			self.buttons.remove(self.header_left)

		if self.fleet_left:
			self.header_left = UIButton(self.fleet_left.name, self.header_left_clicked)
			self.header_left.rect.midbottom = self.list_left.rect.midtop
			self.header_left.rect.y += 1

			self.disband_fleet_left.rect.topleft = self.list_left.rect.bottomleft
			self.disband_fleet_left.rect.move_ip(0, -1)
		else:
			self.header_left = UIButton("No Fleet", self.header_left_clicked)
			self.header_left.rect.midbottom = pos

			self.disband_fleet_left.rect.bottomright = (0, 0)

		self.buttons.append(self.header_left)


	def update_right_list(self):
		if self.list_right:
			selected_index = self.list_right.get_selected_index()
		else:
			selected_index = None

		screen_rect = self._app._surface.get_rect()
		pos = screen_rect.center
		pos = (pos[0] + 160, pos[1])
		if self.fleet_right:
			self.list_right = self.make_list(self.fleet_right, pos)

			if selected_index != None:
				self.list_right.select(selected_index)
		else:
			self.list_right = None

		if self.header_right:
			self.buttons.remove(self.header_right)

		if self.fleet_right:
			self.header_right = UIButton(self.fleet_right.name, self.header_right_clicked)
			self.header_right.rect.midbottom = self.list_right.rect.midtop
			self.header_right.rect.y += 1

			self.disband_fleet_right.rect.topright = self.list_right.rect.bottomright
			self.disband_fleet_right.rect.move_ip(0, -1)
		else:
			self.header_right = UIButton("No Fleet", self.header_right_clicked)
			self.header_right.rect.midbottom = pos
	
			self.disband_fleet_right.rect.bottomright = (0, 0)

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
				if self.popup_left:
					self.popup_left = None
				elif self.popup_right:
					self.popup_right = None
				else:
					self.on_ok_clicked()

		elif (event.type == pygame.MOUSEBUTTONUP):
			if self.popup_left:
				clicked_fleet = self.popup_left.handle_click(event)
				self.popup_left = None
				if clicked_fleet:
					self.left_fleet_selected(clicked_fleet)
			elif self.popup_right:
				clicked_fleet = self.popup_right.handle_click(event)
				self.popup_right = None
				if clicked_fleet:
					self.right_fleet_selected(clicked_fleet)
			elif self.list_left and self.list_left.handle_click(event):
				return
			elif self.list_right and self.list_right.handle_click(event):
				return
			else:
				for button in self.buttons:
					if button.rect.collidepoint(event.pos):
						button.on_click()

	def render(self, surface):

		if self.list_left:
			self.list_left.render(surface)

		if self.list_right:
			self.list_right.render(surface)
		
		for button in self.buttons:
			button.render(surface)

		if self.popup_left:
			self.popup_left.render(surface)
		if self.popup_right:
			self.popup_right.render(surface)

	def header_left_clicked(self):
		fleet_list = self.fleets[:]
		if self.fleet_right:
			fleet_list.remove(self.fleet_right)
		fleet_list.append(NewFleetOption())
		if len(fleet_list) > 0:
			self.popup_left = UIPopup(fleet_list, self.header_left.rect.center)

	def header_right_clicked(self):
		fleet_list = self.fleets[:]
		if self.fleet_left:
			fleet_list.remove(self.fleet_left)
		fleet_list.append(NewFleetOption())
		if len(fleet_list) > 0:
			self.popup_right = UIPopup(fleet_list, self.header_right.rect.center)

	def left_fleet_selected(self, fleet):
		if fleet.name == "New Fleet":
			self.fleet_left = self.player.create_fleet(self.planet)
			self.fleets.append(self.fleet_left)
		else:
			self.fleet_left = fleet
		self.update_left_list()

	def right_fleet_selected(self, fleet):
		if fleet.name == "New Fleet":
			self.fleet_right = self.player.create_fleet(self.planet)
			self.fleets.append(self.fleet_right)
		else:
			self.fleet_right = fleet
		self.update_right_list()

	def on_left_1_clicked(self):
		self.move_left(1)

	def on_left_10_clicked(self):
		self.move_left(10)

	def on_left_100_clicked(self):
		self.move_left(100)

	def move_left(self, amount):
		ship_type = self.list_right.get_selected_item().split("s:")[0]
		if ship_type == "Colony Ship":
			ship_type = "Colony"

		if ship_type:
			ships = self.fleet_right.extract(ship_type, amount)
			for ship in ships:
				self.fleet_left.ships.append(ship)
			self.update_left_list()
			self.update_right_list()

	def on_right_1_clicked(self):
		self.move_right(1)

	def on_right_10_clicked(self):
		self.move_right(10)

	def on_right_100_clicked(self):
		self.move_right(100)

	def move_right(self, amount):
		if not self.fleet_right:
			return

		ship_type = self.list_left.get_selected_item().split("s:")[0]
		if ship_type == "Colony Ship":
			ship_type = "Colony"

		if ship_type:
			ships = self.fleet_left.extract(ship_type, amount)
			for ship in ships:
				self.fleet_right.ships.append(ship)
			self.update_left_list()
			self.update_right_list()

	def on_disband_fleet_left_clicked(self):
		self.player.disband_fleet(self.fleet_left)
		self.fleets.remove(self.fleet_left)

		other_fleets = self.fleets[:]
		if self.fleet_right:
			other_fleets.remove(self.fleet_right)
		if len(other_fleets) == 0:
			self.fleet_left = None
		else:
			self.fleet_left = other_fleets[0]

		self.update_left_list()

	def on_disband_fleet_right_clicked(self):
		self.player.disband_fleet(self.fleet_right)
		self.fleets.remove(self.fleet_right)

		other_fleets = self.fleets[:]
		if self.fleet_left:
			other_fleets.remove(self.fleet_left)
		if len(other_fleets) == 0:
			self.fleet_right = None
		else:
			self.fleet_right = other_fleets[0]

		self.update_right_list()

	def on_ok_clicked(self):
		screen = self._app.screens.change_to(self.prev_screen_name)
		screen.setup(self.planet)

		if self.fleet_left:
			screen.selected_fleet = self.fleet_left
		elif len(self.fleets) > 0:
			screen.selected_fleet = self.fleets[0]
		else:
			screen.selected_fleet = None
