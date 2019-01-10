import random

sizes = ["Tiny", "Small", "Medium", "Large", "Huge"]
types = ["Baren", "Arid", "Terran", "Rich", "Gaïa"]
suffixes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"]

class Planet:

	def __init__(self, star):
		self.star = star
		self.size = sizes[random.randrange(0,len(sizes))]
		self.type = types[random.randrange(0,len(types))]
		self.name = star.name + " " + suffixes[len(star.planets)]
		self.player = None

	def colonize(self, player):
		if (self.player) return false

		self.player = player
		return true