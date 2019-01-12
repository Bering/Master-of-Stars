class PlayerBase:

	def __init__(self, name):
		self.name = name
		self.planets = []
		self.selected_star = None
		self.selected_planet = None
		self.selected_planet_index = 0

	def select_star(self, star):
		self.selected_star = star

	def select_planet(self, planet):
		self.select_star(planet.star)
		self.selected_planet = planet

	def next_planet(self):
		self.selected_planet_index += 1
		if (self.selected_planet_index == len(self.planets)):
			self.selected_planet_index = 0
		self.select_planet(self.planets[self.selected_planet_index])

	def prev_planet(self):
		self.selected_planet_index -= 1
		if (self.selected_planet_index < 0):
			self.selected_planet_index = len(self.planets) - 1
		self.select_planet(self.planets[self.selected_planet_index])

	def colonize_planet(self, planet):
		self.planets.append(planet)
		planet.colonize(self)
