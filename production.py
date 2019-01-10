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

		self.produce(planet, item_count)

	def produce(self, planet, item_count):
		pass

class ProdPop(ProductionBase):

	def __init__(self):
		super().__init__("Population", 5)

	def produce(self, planet, item_count):
		planet.population ++

class ProdInd(ProductionBase):

	def __init__(self):
		super().__init__("Industry", 5)

	def produce(self, planet, item_count):
		planet.industry ++

class ProdSci(ProductionBase):

	def __init__(self):
		super().__init__("Science", 5)

	def produce(self, planet, item_count):
		planet.science ++

class ProdDef(ProductionBase):

	def __init__(self):
		super().__init__("Defense", 10)

	def produce(self, planet, item_count):
		planet.defense ++

class ProdShipyard(ProductionBase):

	def __init__(self):
		super().__init__("Shipyard", 50)

	def produce(self, planet, item_count):
		planet.shipyard_level ++

#class ProdFrigate(ProductionBase):

#	def __init__(self):
#		super().__init__("Frigate", 10)

#	def produce(self, planet, item_count):
#		planet.build_ship("Frigate")