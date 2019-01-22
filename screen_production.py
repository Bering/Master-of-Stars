from screen_base import ScreenBase
from text_renderer import TextRenderer
from tile_renderer import TileRenderer
import pygame
import os

class ProductionScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		self.selected_planet = None

		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 16)
		text_renderer = TextRenderer(font)
		self.tile_renderer = TileRenderer(text_renderer)

		self.tiles = {}

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
				self._app.screens.change_to("Quit")
			if event.key == pygame.K_ESCAPE:
				self._app.screens.change_back()
		elif event.type == pygame.MOUSEBUTTONUP:
			for project, tile_rect in self.tiles.items():
				if tile_rect.collidepoint(event.pos):
					self.change_production(project)

	def render(self, surface):

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

		project = self.selected_planet.production.projects["Scout"]
		scout_surface = self.render_tile(project, (255,200,200))
		scout_rect = scout_surface.get_rect()
		scout_rect.topright = surface.get_rect().topright
		scout_rect.move_ip(-32, 32)
		surface.blit(scout_surface, scout_rect)
		self.tiles["Scout"] = scout_rect

		project = self.selected_planet.production.projects["Colony"]
		colony_surface = self.render_tile(project, (255,255,255))
		colony_rect = colony_surface.get_rect()
		colony_rect.topright = scout_rect.bottomright
		colony_rect.move_ip(0, 6)
		surface.blit(colony_surface, colony_rect)
		self.tiles["Colony"] = colony_rect

		project = self.selected_planet.production.projects["Frigate"]
		frigate_surface = self.render_tile(project, (255,200,200))
		frigate_rect = frigate_surface.get_rect()
		frigate_rect.topright = colony_rect.bottomright
		frigate_rect.move_ip(0, 6)
		surface.blit(frigate_surface, frigate_rect)
		self.tiles["Frigate"] = frigate_rect

		project = self.selected_planet.production.projects["Destroyer"]
		destroyer_surface = self.render_tile(project, (255,200,200))
		destroyer_rect = destroyer_surface.get_rect()
		destroyer_rect.topright = frigate_rect.bottomright
		destroyer_rect.move_ip(0, 6)
		surface.blit(destroyer_surface, destroyer_rect)
		self.tiles["Destroyer"] = destroyer_rect

	def select_planet(self, planet):
		self.selected_planet = planet

	def render_tile(self, project, color=(255,255,255)):
		text = ""
		text += project.name + "\n"
		text += project.desc + "\n"
		text += "Cost: " + str(project.cost)
		return self.tile_renderer.render(text, color)

	def change_production(self, project):
		self.selected_planet.production.change_to(project)
		self._app.screens.change_back()
