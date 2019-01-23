from screen_base import ScreenBase
from text_renderer import TextRenderer
from tile_renderer import TileRenderer
from button import Button

import pygame
import os

class ResearchScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_planet = None

		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 16)
		text_renderer = TextRenderer(font)
		self.tile_renderer = TileRenderer(text_renderer)

		self.tiles = {}

		self.back_button = Button("Cancel", self.on_back_button_clicked)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if event.key == pygame.K_ESCAPE:
				self.on_back_button_clicked()
		elif event.type == pygame.MOUSEBUTTONUP:
			for project_name, tile_rect in self.tiles.items():
				if tile_rect.collidepoint(event.pos):
					self.change_project(project_name)
			if self.back_button.rect.collidepoint(event.pos):
				self.back_button.on_click()

	def render(self, surface):

		self.back_button.rect.midbottom = surface.get_rect().midbottom
		self.back_button.rect.move_ip(0, -32)
		self.back_button.render(surface)

		anchor = surface.get_rect().topleft
		anchor = anchor[0] + 32, anchor[1] + 32

		if self.selected_planet.player.tech_levels["Shipyard"] < 3:
			project = self.selected_planet.player.research_projects["Shipyard"]
			sy_surface = self.render_tile(project)
			sy_rect = sy_surface.get_rect()
			sy_rect.topleft = anchor
			surface.blit(sy_surface, sy_rect)
			self.tiles["Shipyard"] = sy_rect

		anchor = surface.get_rect().topright
		anchor = anchor[0] - 32, anchor[1] + 32

		project = self.selected_planet.player.research_projects["Scout"]
		scout_surface = self.render_tile(project, (255,200,200))
		scout_rect = scout_surface.get_rect()
		scout_rect.topright = anchor
		surface.blit(scout_surface, scout_rect)
		self.tiles["Scout"] = scout_rect

		anchor = scout_rect.bottomright
		anchor = anchor[0], anchor[1] + 6

		project = self.selected_planet.player.research_projects["Colony"]
		colony_surface = self.render_tile(project, (255,255,255))
		colony_rect = colony_surface.get_rect()
		colony_rect.topright = anchor
		surface.blit(colony_surface, colony_rect)
		self.tiles["Colony"] = colony_rect

		anchor = colony_rect.bottomright
		anchor = anchor[0], anchor[1] + 6

		project = self.selected_planet.player.research_projects["Frigate"]
		frigate_surface = self.render_tile(project, (255,200,200))
		frigate_rect = frigate_surface.get_rect()
		frigate_rect.topright = anchor
		surface.blit(frigate_surface, frigate_rect)
		self.tiles["Frigate"] = frigate_rect

		anchor = frigate_rect.bottomright
		anchor = anchor[0], anchor[1] + 6

		project = self.selected_planet.player.research_projects["Destroyer"]
		destroyer_surface = self.render_tile(project, (255,200,200))
		destroyer_rect = destroyer_surface.get_rect()
		destroyer_rect.topright = anchor
		surface.blit(destroyer_surface, destroyer_rect)
		self.tiles["Destroyer"] = destroyer_rect

	def select_planet(self, planet):
		self.selected_planet = planet

	def on_back_button_clicked(self):
		self._app.screens.change_to("Planet")

	def render_tile(self, project, color=(255,255,255)):
		text = ""
		text += project.name + "\n"
		text += project.desc + "\n"
		text += "Cost: " + str(project.cost)
		return self.tile_renderer.render(text, color)

	def change_project(self, project_name):
		self.selected_planet.set_research(project_name)
		self._app.screens.change_to("Planet")
