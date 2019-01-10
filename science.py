class ResearchBase:

	def __init__(self, name, cost):
		self.name = name
		self.cost = cost
		self.progress = 0

	def next_turn(self, planet):
		self.progress += planet.science

		item_count = 0

		while(self.progress > self.cost):
			self.progress -= self.cost
			item_count ++

		self.effect(planet, item_count)

	def effect(self, planet, item_count):
		pass

class ResearchShipyard(ResearchBase):

	def __init__(self, planet):
		super().__init__("Upgrade Shipyard", 50 * planet.shipyard_level)

	def effect(self, planet, item_count):
		planet.shipyard_level += item_count

#class ResearchFrigate(ResearchBase):

#	def __init__(self, planet):
#		super().__init__("Upgrade Fighters", 50 * planet.fighters_level)

#	def effect(self, planet, item_count):
#		planet.fighters_level += item_count
