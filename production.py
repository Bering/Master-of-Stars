class ProductionManager:

	def __init__(self, planet):
		self.projects = {
			"Population" : ProdPop(planet),
			"Industry" : ProdInd(planet),
			"Science" : ProdSci(planet),
			"Defences" : ProdDef(planet),
			"Scout" : ProdScout(planet)
		}
		self.current_project = None

	def change_to(project_name):
		if project_name not in self.self.projects:
			raise KeyError("Invalid production project name: " + project_name)

		self.current_project = self.projects[project_name]
		self.current_project.change_to()

	def next_turn(self):
		if self.current_project:
			self.current_project.next_turn()


class ProductionBase:

	def __init__(self, planet, name, cost):
		self.planet = planet
		self.name = name
		self.cost = cost
		self.progress = 0

	def change_to(self):
		# TODO: Should we keep the progress made during the previous project?
		self.progress = 0

	def next_turn(self):
		self.progress += self.planet.industry

		item_count = 0

		while(self.progress > self.cost):
			self.progress -= self.cost
			item_count += 1

		self.effect(item_count)

	def effect(self, item_count):
		pass


class ProdPop(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Population", 5)

	def effect(self, item_count):
		self.planet.population += item_count

class ProdInd(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Industry", 5)

	def effect(self, item_count):
		self.planet.industry += item_count

class ProdSci(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Science", 5)

	def effect(self, item_count):
		self.planet.science += item_count

class ProdDef(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Defense", 10)

	def effect(self, item_count):
		self.planet.defense += item_count

class ProdScout(ProductionBase):

	def __init__(self, planet):
		super().__init__(planet, "Ship: Scout", 10)

	def effect(self, item_count):
		for n in range(item_count):
			self.planet.build_ship("Scout")

# TODO: Fighter, Frigate, Destroyer, Colony, Starbases, more, Refit
