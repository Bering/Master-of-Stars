from fleet import Fleet
import research

class PlayerBase:

	def __init__(self, name):
		self.name = name
		self.planets = []
		self.selected_planet_index = 0
		self.fleets = []
		self.fleets_counter = 0
		self.tech_levels = {
			"Shipyard" : 1,
			"Scout" : 1,
			"Frigate" : 0,
			"Destroyer" : 0,
			"Colony" : 0
		}
		self.research_projects = {
			"Shipyard" : research.ResearchShipyard(self),
			"Scout" : research.ResearchScout(self),
			"Frigate" : research.ResearchFrigate(self),
			"Destroyer" : research.ResearchDestroyer(self),
			"Colony" : research.ResearchColony(self)
		}

	def next_planet(self, current_planet):
		if current_planet == None:
			self.selected_planet_index = 0
		else:
			self.selected_planet_index = self.planets.index(current_planet) + 1

		if (self.selected_planet_index == len(self.planets)):
			self.selected_planet_index = 0

		return self.planets[self.selected_planet_index]

	def prev_planet(self, current_planet):
		if current_planet == None:
			self.selected_planet_index = 0
		else:
			self.selected_planet_index = self.planets.index(current_planet) - 1

		if (self.selected_planet_index < 0):
			self.selected_planet_index = len(self.planets) - 1

		return self.planets[self.selected_planet_index]

	def found_colony(self, planet, fleet):
		self.planets.append(planet)
		planet.found_colony(self, fleet)

	# TODO: This requires a planet but I want to be able to manage fleets in orbit around stars
	def create_fleet(self, planet):
		self.fleets_counter += 1
		fleet = Fleet(planet, self.fleets_counter)
		self.fleets.append(fleet)
		planet.star.fleets.append(fleet)
		planet.fleets.append(fleet)
		return fleet

	def disband_fleet(self, fleet):
		fleet.planet.fleets.remove(fleet)
		fleet.planet.star.fleets.remove(fleet)
		self.fleets.remove(fleet)
		fleet.ships.clear()
	