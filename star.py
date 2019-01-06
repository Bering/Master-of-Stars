from planet import Planet

class Star:

	def __init__(self, name):
		self.name = name
		self.planets = []

	def addPlanet(self):
		p = Planet(self)
		self.planets.append(p)
