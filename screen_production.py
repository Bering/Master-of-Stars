from screen_base import ScreenBase
from ui_text_renderer import UITextRenderer
from ui_tile_renderer import UITileRenderer
from ui_button import UIButton

import pygame
import os

class ProductionScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_planet = None

		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 16)
		text_renderer = UITextRenderer(font)
		self.tile_renderer = UITileRenderer(text_renderer)

		self.tiles = {}

		self.back_button = UIButton("Cancel", self.on_back_button_clicked)

	def setup(self, planet):
		self.selected_planet = planet

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
				self.on_back_button_clicked()
		elif event.type == pygame.MOUSEBUTTONUP:
			for project_name, tile_rect in self.tiles.items():
				if tile_rect.collidepoint(event.pos):
					self.change_production(project_name)
			if self.back_button.rect.collidepoint(event.pos):
				self.back_button.on_click()

	def render(self, surface):

		self.back_button.rect.midbottom = surface.get_rect().midbottom
		self.back_button.rect.move_ip(0, -32)
		self.back_button.render(surface)

		project = self.selected_planet.production.projects["Farms"]
		farm_surface = self.render_tile(project)
		farm_rect = farm_surface.get_rect()
		farm_rect.move_ip(32,32)
		surface.blit(farm_surface, farm_rect)
		self.tiles["Farms"] = farm_rect

		project = self.selected_planet.production.projects["Mines"]
		mine_surface = self.render_tile(project, (255,255,200))
		mine_rect = mine_surface.get_rect()
		mine_rect.topleft = farm_rect.bottomleft
		mine_rect.move_ip(0, 6)
		surface.blit(mine_surface, mine_rect)
		self.tiles["Mines"] = mine_rect

		project = self.selected_planet.production.projects["Laboratories"]
		lab_surface = self.render_tile(project, (200,200,255))
		lab_rect = lab_surface.get_rect()
		lab_rect.topleft = mine_rect.bottomleft
		lab_rect.move_ip(0, 6)
		surface.blit(lab_surface, lab_rect)
		self.tiles["Laboratories"] = lab_rect

		project = self.selected_planet.production.projects["Defenses"]
		def_surface = self.render_tile(project, (255,200,200))
		def_rect = def_surface.get_rect()
		def_rect.topleft = lab_rect.bottomleft
		def_rect.move_ip(0, 6)
		surface.blit(def_surface, def_rect)
		self.tiles["Defenses"] = def_rect

		anchor = surface.get_rect().topright
		anchor = anchor[0] - 32, anchor[1] + 32

		if self.selected_planet.shipyard_level == 0:
			project = self.selected_planet.production.projects["Shipyard1"]
			sy_surface = self.render_tile(project, (255,200,200))
			sy_rect = sy_surface.get_rect()
			sy_rect.topright = anchor
			surface.blit(sy_surface, sy_rect)
			self.tiles["Shipyard1"] = sy_rect

			anchor = sy_rect.bottomright
			anchor = anchor[0], anchor[1] + 6

		if (self.selected_planet.player.tech_levels["Shipyard"] >= 2) \
			and (self.selected_planet.shipyard_level == 1):
			project = self.selected_planet.production.projects["Shipyard2"]
			sy_surface = self.render_tile(project, (255,200,200))
			sy_rect = sy_surface.get_rect()
			sy_rect.topright = anchor
			surface.blit(sy_surface, sy_rect)
			self.tiles["Shipyard2"] = sy_rect

			anchor = sy_rect.bottomright
			anchor = anchor[0], anchor[1] + 6

		if (self.selected_planet.player.tech_levels["Shipyard"] >= 3) \
			and (self.selected_planet.shipyard_level == 2):
			project = self.selected_planet.production.projects["Shipyard3"]
			sy_surface = self.render_tile(project, (255,200,200))
			sy_rect = sy_surface.get_rect()
			sy_rect.topright = anchor
			surface.blit(sy_surface, sy_rect)
			self.tiles["Shipyard3"] = sy_rect

			anchor = sy_rect.bottomright
			anchor = anchor[0], anchor[1] + 6

		if self.selected_planet.shipyard_level >= 1:
			project = self.selected_planet.production.projects["Scout"]
			scout_surface = self.render_tile(project, (255,200,200))
			scout_rect = scout_surface.get_rect()
			scout_rect.topright = anchor
			surface.blit(scout_surface, scout_rect)
			self.tiles["Scout"] = scout_rect

			anchor = scout_rect.bottomright
			anchor = anchor[0], anchor[1] + 6

		if self.selected_planet.shipyard_level >= 3 \
		and self.selected_planet.player.tech_levels["Colony"] > 0:
			project = self.selected_planet.production.projects["Colony"]
			colony_surface = self.render_tile(project, (255,255,255))
			colony_rect = colony_surface.get_rect()
			colony_rect.topright = anchor
			surface.blit(colony_surface, colony_rect)
			self.tiles["Colony"] = colony_rect

			anchor = colony_rect.bottomright
			anchor = anchor[0], anchor[1] + 6

		if self.selected_planet.shipyard_level >= 2 \
		and self.selected_planet.player.tech_levels["Frigate"] > 0:
			project = self.selected_planet.production.projects["Frigate"]
			frigate_surface = self.render_tile(project, (255,200,200))
			frigate_rect = frigate_surface.get_rect()
			frigate_rect.topright = anchor
			surface.blit(frigate_surface, frigate_rect)
			self.tiles["Frigate"] = frigate_rect

			anchor = frigate_rect.bottomright
			anchor = anchor[0], anchor[1] + 6

		if self.selected_planet.shipyard_level >= 3 \
		and self.selected_planet.player.tech_levels["Destroyer"] > 0:
			project = self.selected_planet.production.projects["Destroyer"]
			destroyer_surface = self.render_tile(project, (255,200,200))
			destroyer_rect = destroyer_surface.get_rect()
			destroyer_rect.topright = anchor
			surface.blit(destroyer_surface, destroyer_rect)
			self.tiles["Destroyer"] = destroyer_rect

	def render_tile(self, project, color=(255,255,255)):
		text = ""
		text += project.name + "\n"
		text += project.desc + "\n"
		text += "Cost: " + str(project.cost)
		return self.tile_renderer.render(text, color)

	def on_back_button_clicked(self):
		self._app.screens.change_to("Planet")

	def change_production(self, project):
		self.selected_planet.production.change_to(project)
		self._app.screens.change_to("Planet")
