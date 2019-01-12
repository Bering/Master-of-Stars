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

		self.effect(planet, item_count)

	def effect(self, planet, item_count):
		pass

class ProdPop(ProductionBase):

	def __init__(self):
		super().__init__("Population", 5)

	def effect(self, planet, item_count):
		planet.population += item_count

class ProdInd(ProductionBase):

	def __init__(self):
		super().__init__("Industry", 5)

	def effect(self, planet, item_count):
		planet.industry += item_count

class ProdSci(ProductionBase):

	def __init__(self):
		super().__init__("Science", 5)

	def effect(self, planet, item_count):
		planet.science += item_count

class ProdDef(ProductionBase):

	def __init__(self):
		super().__init__("Defense", 10)

	def effect(self, planet, item_count):
		planet.defense += item_count

class ProdFrigate(ProductionBase):

	def __init__(self):
		super().__init__("Frigate", 10)

	def effect(self, planet, item_count):
		for n in range(item_count):
			planet.build_ship("Frigate")
