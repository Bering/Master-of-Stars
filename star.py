from planet import Planet

names = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]

class Star:

	def __init__(self, name):
		self.name = name
		self.planets = []

	def addPlanet(self):
		name = self.name + " " + names[len(self.planets)]
		planet = Planet(self, name)
		self.planets.append(planet)
