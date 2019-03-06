import os
import math
import pygame
import icon
from screen_base import ScreenBase
from ui_button import UIButton
from ui_text_renderer import UITextRenderer
from ui_tile_renderer import UITileRenderer
from ui_popup import UIPopup

class PlanetScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.planet = None

		self.name_font = pygame.font.Font(None, 18)
		
		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		info_font = pygame.font.Font(filename, 16)
		text_renderer = UITextRenderer(info_font)
		self.tile_renderer = UITileRenderer(text_renderer)

		self.button_production = UIButton("Change", self.on_change_production_clicked)
		self.button_research = UIButton("Change", self.on_change_research_clicked)
		self.button_colonize = UIButton("Colonize", self.on_colonize_clicked)
		self.button_next_turn = UIButton("End Turn", self.on_next_turn_clicked)
		self.button_fleet = UIButton("Manage", self.on_fleet_manage_clicked)

		self.buttons = [
			self.button_production,
			self.button_research,
			self.button_colonize,
			self.button_next_turn,
			self.button_fleet
		]

		self.fleet_selection_popup = None
		self.fleet_info_rect = None
		self.selected_fleet = None
		
	def setup(self, planet):
		self.planet = planet

		self.centered_rect = planet.rect.copy()
		self.centered_rect.width *= 3
		self.centered_rect.height *= 3
		self.centered_surface = pygame.transform.smoothscale(planet.surface, self.centered_rect.size)

		self.name_surf = self.name_font.render(self.planet.name, True, (255,255,255))
		self.name_rect = self.name_surf.get_rect()

		if planet.player:
			surface = planet.player.icon_ownermarker
			self.ownermarker_rect = surface.get_rect()
			self.ownermarker_rect.width *= 3
			self.ownermarker_rect.height *= 3
			self.ownermarker = pygame.transform.smoothscale(surface, self.ownermarker_rect.size)

			surface = planet.player.icon_shipyard
			self.shipyard_rect = surface.get_rect()
			self.shipyard_rect.width *= 2
			self.shipyard_rect.height *= 2
			self.shipyard_surface = pygame.transform.smoothscale(surface, self.shipyard_rect.size)

			surface = planet.player.icon_defense
			self.defense_rect = surface.get_rect()
			self.defense_rect.width *= 2
			self.defense_rect.height *= 2
			self.defense_surface = pygame.transform.smoothscale(surface, self.defense_rect.size)

		self.player_fleets = []
		self.enemy_fleets = []
		for f in self.planet.fleets:
			if f.player == self._app.local_player:
				self.player_fleets.append(f)
			else:
				self.enemy_fleets.append(f)

		if self.player_fleets:
			self.selected_fleet = self.player_fleets[0]
		elif self.planet.fleets:
			self.selected_fleet = self.planet.fleets[0]
		else:
			self.selected_fleet = None

		if self.player_fleets:
			surface = self.player_fleets[0].surface
			self.fleet_rect = surface.get_rect()
			self.fleet_rect.width *= 2
			self.fleet_rect.height *= 2
			self.fleet_surface = pygame.transform.smoothscale(surface, self.fleet_rect.size)

		if self.enemy_fleets:
			surface = self.enemy_fleets[0].surface
			self.enemy_fleet_rect = surface.get_rect()
			self.enemy_fleet_rect.width *= 2
			self.enemy_fleet_rect.height *= 2
			self.enemy_fleet_surface = pygame.transform.smoothscale(surface, self.enemy_fleet_rect.size)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
				self.on_next_turn_clicked()
			elif (event.key == pygame.K_g):
				self._app.screens.change_to("Galaxy")
			elif (event.key == pygame.K_s):
				self._app.screens.change_to("Star")
			elif (event.key == pygame.K_r):
				self.on_change_research_clicked()
			elif (event.key == pygame.K_p):
				self.on_change_production_clicked()
			elif (event.key == pygame.K_f):
				self.on_fleet_manage_clicked()
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
				self.selected_fleet = self.fleet_selection_popup.handle_click(event)
				self.fleet_selection_popup = None
			else:
				if self.centered_rect.collidepoint(event.pos):
					self.on_planet_clicked()
				else:
					if len(self.player_fleets) > 1:
						if self.fleet_info_rect.collidepoint(event.pos) \
						or self.enemy_fleet_info_rect.collidepoint(event.pos) \
						or self.fleet_rect.collidepoint(event.pos):
							self.fleet_selection_popup = UIPopup(
								self.player_fleets,
								event.pos
							)
					for b in self.buttons:
						if b.rect.collidepoint(event.pos):
							b.on_click()

	def update(self, delta_time):
		pass

	def render(self, surface):
		self.centered_rect.center = surface.get_rect().center
		surface.blit(self.centered_surface, self.centered_rect)

		if self.planet.player:
			self.ownermarker_rect.center = surface.get_rect().center
			surface.blit(self.ownermarker, self.ownermarker_rect)

		if self.player_fleets:
			self.fleet_rect.midleft = self.centered_rect.topright
			surface.blit(self.fleet_surface, self.fleet_rect)

		if self.enemy_fleets:
			self.enemy_fleet_rect.midbottom = self.centered_rect.topright
			surface.blit(self.enemy_fleet_surface, self.enemy_fleet_rect)

		if self.planet.shipyard_level > 0:
			self.shipyard_rect.midleft = self.centered_rect.bottomright
			surface.blit(self.shipyard_surface, self.shipyard_rect)

		if self.planet.defense > 0:
			self.defense_rect.midright = self.centered_rect.bottomleft
			surface.blit(self.defense_surface, self.defense_rect)

		# Planet name
		self.name_rect.midtop = self.centered_rect.midbottom
		surface.blit(self.name_surf, self.name_rect)

		# Planet info
		info_surface = self.render_info_text()
		info_rect = info_surface.get_rect()
		info_rect.bottomright = self.centered_rect.topleft
		info_rect.move_ip(-32, -32)
		surface.blit(info_surface, info_rect)

		# Colonize button
		if self.planet.player:
			self.button_colonize.rect.bottomright = (0, 0)
		elif self.planet.fleets and self.selected_fleet.get_ship_counts()["Colony"] > 0:
			self.button_colonize.rect.midtop = info_rect.midbottom
			self.button_colonize.rect.move_ip(0, 6)
			self.button_colonize.render(surface)

		# Fleet info
		fleet_surface = self.render_fleet_text()
		self.fleet_info_rect = fleet_surface.get_rect() # self. because of the fleet selection popup
		self.fleet_info_rect.bottomleft = self.centered_rect.topright
		self.fleet_info_rect.move_ip(32, -32)
		surface.blit(fleet_surface, self.fleet_info_rect)

		if self.player_fleets:
			self.button_fleet.rect.midtop = self.fleet_info_rect.midbottom
			self.button_fleet.rect.move_ip(0, 6)
			self.button_fleet.render(surface)
		else:
			self.button_fleet.rect.bottomright = (0, 0)

		if self.planet.player:

			# Research info
			research_surface = self.render_research_text()
			research_rect = research_surface.get_rect()
			research_rect.topright = self.centered_rect.bottomleft
			research_rect.move_ip(-32, 32)
			surface.blit(research_surface, research_rect)

			if self.planet.player == self._app.local_player:
				self.button_research.rect.midtop = research_rect.midbottom
				self.button_research.rect.move_ip(0, 6)
				self.button_research.render(surface)

			# Production info
			production_surface = self.render_production_text()
			production_rect = production_surface.get_rect()
			production_rect.topleft = self.centered_rect.bottomright
			production_rect.move_ip(32, 32)
			surface.blit(production_surface, production_rect)

			if self.planet.player == self._app.local_player:
				self.button_production.rect.midtop = production_rect.midbottom
				self.button_production.rect.move_ip(0, 6)
				self.button_production.render(surface)

		self.button_next_turn.rect.topright = surface.get_rect().topright
		self.button_next_turn.rect.move_ip(-16, 16)
		self.button_next_turn.render(surface)

		if self.fleet_selection_popup:
			self.fleet_selection_popup.render(surface)

	def render_info_text(self):
		text = ""
		text += "Class: " + self.planet.size + " " + self.planet.type + "\n"
		text += "Population: " + str(self.planet.population) + "\n"
		text += "Industry: " + str(self.planet.industry) + "\n"
		text += "Science: " + str(self.planet.science) + "\n"
		text += "Defense: " + str(self.planet.defense) + "\n"

		if self.planet.shipyard_level == 0:
			text += "Shipyard: None"
		else:
			text += "Shipyard: Lvl." + str(self.planet.shipyard_level)

		return self.tile_renderer.render(text, (255,255,255))

	def render_research_text(self):
		if self.planet.current_research_project == None:
			text = ""
			text += "Researching:\n"
			text += "(Nothing)\n"
			text += "Cost: N/A\n"
			text += "Progress: N/A"
			return self.tile_renderer.render(text, (200,200,255))

		text = ""
		text += "Researching:\n"
		text += self.planet.current_research_project.name + "\n"
		text += "Cost: " + str(self.planet.current_research_project.cost) + "\n"

		if self.planet.current_research_project.progress < self.planet.current_research_project.cost:
			text += "Progress: " + str(self.planet.current_research_project.progress) + "\n"
		else:
			text += "Progress: COMPLETE!"

		return self.tile_renderer.render(text, (200,200,255))

	def render_production_text(self):
		if self.planet.production.current_project == None:
			text = ""
			text += "Producing:\n"
			text += "(Nothing)\n"
			text += "Cost: N/A\n"
			text += "Progress: N/A\n"
			text += "ETA: N/A\n"
			return self.tile_renderer.render(text, (255,255,200))

		if self.planet.industry == 0:
			remaining_turns = "N/A"
		else:
			remaining_turns = str(math.ceil(
				(self.planet.production.current_project.cost
				- self.planet.production.current_project.progress)
				/ self.planet.industry
			)) + " turn(s)"
		text = ""
		text += "Producing:\n"
		text += self.planet.production.current_project.name + "\n"
		text += "Cost: " + str(self.planet.production.current_project.cost) + "\n"
		text += "Progress: " + str(self.planet.production.current_project.progress) + "\n"
		text += "ETA: " + remaining_turns + "\n"
		return self.tile_renderer.render(text, (255,255,200))

	def render_fleet_text(self):
		if not self.planet.fleets:
			text = "No fleet"
		else:
			ship_counts = self.selected_fleet.get_ship_counts()
			text = ""
			text += self.selected_fleet.name + "\n"
			text += "Scout(s): " + str(ship_counts["Scout"]) + "\n"
			text += "Colony Ship(s): " + str(ship_counts["Colony"]) + "\n"
			text += "Frigate(s): " + str(ship_counts["Frigate"]) + "\n"
			text += "Destroyer(s): " + str(ship_counts["Destroyer"]) + "\n"
			text += "Total: " + str(ship_counts["Total"])

		return self.tile_renderer.render(text, (255,200,200))

	def on_next_turn_clicked(self):
		self._app.next_turn()

	def on_planet_clicked(self):
		self._app.screens.change_to("Star")

	def on_change_production_clicked(self):
		s = self._app.screens.change_to("Production")
		s.setup(self.planet)

	def on_change_research_clicked(self):
		s = self._app.screens.change_to("Research")
		s.setup(self.planet)

	def on_fleet_manage_clicked(self):
		if self.player_fleets:
			s = self._app.screens.change_to("Fleet")
			s.setup("Planet", self.selected_fleet)

	def on_colonize_clicked(self):
		self.planet.player.found_colony(self.planet, self.selected_fleet)

	def on_next_planet(self):
		self.select_planet(self._app.local_player.next_planet(self.selected_planet).star)

	def on_prev_planet(self):
		self.select_planet(self._app.local_player.prev_planet(self.selected_planet).star)
