import random

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
_production_bonuses = {
	"Baren" : { "pop": 0, "ind": 0, "sci": 0 },
	"Arid" : { "pop": 0, "ind": 0, "sci": 0 },
	"Terran" : { "pop": 1, "ind": 0, "sci": 0 },
	"Rich" : { "pop": 0, "ind": 1, "sci": 0 },
	"Gaia" : { "pop": 2, "ind": 2, "sci": 1 }
}

class Planet:

	def __init__(self, star):
		self.star = star
		self.name = star.name + " " + _suffixes[len(star.planets)]
		self.player = None
		self.size = _sizes[random.randrange(0,len(_sizes))]
		self.type = _types[random.randrange(0,len(_types))]
		self.population = 0
		self.industry = 0
		self.science = 0
		self.defense = 0
		self.shipyard_level = 0

	def colonize(self, player):
		if (self.player): return False

		self.player = player
		self.population = 1
		self.population += _production_bonuses[self.type]["pop"]
		self.industry += _production_bonuses[self.type]["ind"]
		self.science += _production_bonuses[self.type]["sci"]
		return True
	
	def set_production(self, production):
		self.production = production

	def set_research(self, research):
		self.research = research
	