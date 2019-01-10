class PlayerBase:

	def __init__(self, name):
		self.name = name
		self.planets = []

	def colonize_planet(self, planet):
		self.planets.append(planet)
		planet.colonize(self)
