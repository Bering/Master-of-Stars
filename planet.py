import production
import random
import pygame
import os

_sizes = ["Tiny", "Small", "Medium", "Large", "Huge"]
_types = ["Baren", "Arid", "Terran", "Rich", "Gaia"]
_suffixes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]
_population_limits = {
	"Tiny" : 10,
	"Small" : 100,
	"Medium" : 1000,
	"Large" : 10000,
	"Huge" : 100000
}

class Planet:

	def __init__(self, star, x, y):
		self.star = star
		self.name = star.name + " " + _suffixes[len(star.planets)]
		self.size = _sizes[random.randrange(len(_sizes))]
		self.type = _types[random.randrange(len(_types))]
		self.population_limit = _population_limits[self.size]
		self.player = None
		self.fleets = []
		self.production = production.ProductionManager(self)
		self.current_research_project = None
		
		self.population = 0
		self.industry = 0
		self.science = 0
		self.defense = 0
		self.shipyard_level = 0

		n = random.randrange(8) + 1 # TODO: Pick image based on type and size
		image_file = os.path.join("images", "planet" + str(n) + ".png")
		self.surface = pygame.image.load(image_file).convert_alpha()
		self.rect = self.surface.get_rect().move(x, y)

		font = pygame.font.Font(None, 18)
		render_name = self.name.replace(self.star.name + " ", "")
		self.name_surf = font.render(render_name, True, (255,255,255))
		self.name_rect = self.name_surf.get_rect()
		self.name_rect.midtop = self.rect.midbottom

	def found_colony(self, player, fleet):
		best_colony_ship = fleet.get_best_ship("Colony")
		fleet.destroy_ship(best_colony_ship)
		if fleet.get_ship_counts()["Total"] == 0:
			player.disband_fleet(fleet)

		self.player = player
		self.population = best_colony_ship.tech_level
		self.industry = best_colony_ship.tech_level
		self.population = 1
		self.industry = 1
		self.science = 0
		return True

	def build_ship(self, ship_type):
		if not self.fleets:
			fleet = self.player.create_fleet(self)

		fleet = self.fleets[0]
		fleet.create_ship(ship_type, self.player.tech_levels[ship_type])

	def set_research(self, project_name):
		self.current_research_project = self.player.research_projects[project_name]
		self.current_research_project.is_complete = False
	
	def next_turn(self):
		if (self.production):
			self.production.next_turn()
		
		if (self.current_research_project):
			self.current_research_project.next_turn(self.science)
			if self.current_research_project.is_complete:
				self.current_research_project = None
