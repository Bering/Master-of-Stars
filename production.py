class ProductionBase:

	def __init__(self, name, cost):
		self.name = name
		self.cost = cost
		self.progress = 0

	def next_turn(self, planet):
		self.progress += planet.industry

		item_count = 0

		while(self.progress > self.cost):
			self.progress -= self.cost
			item_count ++

		


class ProdPop(ProductionBase):

	def __init__(self):
		super().__init__("Population", 5)

	def next_turn(self, planet):
		planet.population ++

class ProdInd(ProductionBase):

	def __init__(self):
		super().__init__("Industry", 5)

	def next_turn(self, planet):
		planet.industry ++

class ProdSci(ProductionBase):

	def __init__(self):
		super().__init__("Science", 5)

	def next_turn(self, planet):
		planet.science ++

class ProdDef(ProductionBase):

	def __init__(self):
		super().__init__("Defense", 10)

	def next_turn(self, planet):
		planet.defense ++

class ProdShipyard(ProductionBase):

	def __init__(self):
		super().__init__("Shipyard", 50)

	def next_turn(self, planet):
		planet.shipyard_level ++

#class ProdFrigate(ProductionBase):

#	def __init__(self):
#		super().__init__("Frigate", 10)

#	def next_turn(self, planet):
#		planet.build_ship("Frigate")