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
		super().__init__("Upgrade Shipyard", 50 * planet.tech_levels["Shipyard"])

	def effect(self, planet):
		planet.tech_levels["Shipyard"] ++

class ResearchScout(ResearchBase):

	def __init__(self, planet):
		super().__init__("Upgrade Scouts", 50 * planet.tech_levels["Scout"])

	def effect(self, planet):
		planet.tech_levels["Scout"] ++

class ResearchFrigate(ResearchBase):

	def __init__(self, planet):
		super().__init__("Upgrade Fighters", 50 * planet.tech_levels["Fighter"])

	def effect(self, planet):
		planet.tech_levels["Fighter"] ++

class ResearchDestroyer(ResearchBase):

	def __init__(self, planet):
		super().__init__("Upgrade Destroyers", 50 * planet.tech_levels["Destroyer"])

	def effect(self, planet):
		planet.tech_levels["Destroyer"] ++

class ResearchColony(ResearchBase):

	def __init__(self, planet):
		super().__init__("Upgrade Colony Ships", 50 * planet.tech_levels["Colony"])

	def effect(self, planet):
		planet.tech_levels["Colony"] ++
