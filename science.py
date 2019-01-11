class ResearchBase:

	def __init__(self, name, cost):
		self.name = name
		self.cost = cost
		self.progress = 0

	def next_turn(self, planet):
		self.progress += planet.science

		if(self.progress >= self.cost):
			self.progress = 0
			self.effect(planet)

	def effect(self, planet):
		pass

class ResearchShipyard(ResearchBase):

	def __init__(self, planet):
		super().__init__("Upgrade Shipyard", 50 * planet.shipyard_level)

	def effect(self, planet):
		planet.tech_levels["Shipyard"] ++
		
#class ResearchFrigate(ResearchBase):

#	def __init__(self, planet):
#		super().__init__("Upgrade Fighters", 50 * planet.fighters_level)

#	def effect(self, planet):
#		planet.fighters_level ++
