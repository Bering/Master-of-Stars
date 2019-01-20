class ResearchManager:
	def __init__(self, planet):
		self.planet = planet
		self.tech_levels = {
			"Shipyard" : 1,
			"Defence" : 1,
			"Scout" : 1,
			"Fighter" : 0,
			"Frigate" : 0,
			"Destroyer" : 0,
			"Colony" : 0
		}
		self.projects = {
			"Shipyard" : ResearchShipyard(planet),
			"Defence" : ResearchDefence(planet),
			"Scout" : ResearchScout(planet),
			"Fighter" : ResearchFighter(planet),
			"Frigate" : ResearchFrigate(planet),
			"Destroyer" : ResearchDestroyer(planet),
			"Colony" : ResearchColony(planet)
		}
		self.current_project = None

	def change_to(self, project_name):
		if project_name not in self.projects:
			raise KeyError("Invalid research project name: " + project_name)

		self.current_project = self.projects[project_name]
		self.current_project.change_to()

	def next_turn(self):
		if self.current_project:
			self.current_project.next_turn()


class ResearchBase:

	def __init__(self, planet, name, cost):
		self.planet = planet
		self.name = name
		self.cost = cost
		self.progress = 0

	def change_to(self):
		self.progress = 0

	def next_turn(self):
		self.progress += self.planet.science

		if(self.progress >= self.cost):
			self.effect()

	def effect(self):
		pass


class ResearchShipyard(ResearchBase):

	def __init__(self, planet):
		super().__init__(planet, "Upgrade Shipyard", 50)

	def change_to():
		super().change_to()
		self.cost = 50 * (self.planet.research.tech_levels["Shipyard"] + 1)

	def effect(self):
		self.planet.research.tech_levels["Shipyard"] += 1

class ResearchDefence(ResearchBase):

	def __init__(self, planet):
		super().__init__(planet, "Upgrade Defences", 50)

	def change_to():
		super().change_to()
		self.cost = 50 * (self.planet.research.tech_levels["Defence"] + 1)

	def effect(self):
		self.planet.research.tech_levels["Defence"] += 1

class ResearchScout(ResearchBase):

	def __init__(self, planet):
		super().__init__(planet, "Upgrade Scouts", 50)

	def change_to():
		super().change_to()
		self.cost = 50 * (self.planet.research.tech_levels["Scout"] + 1)

	def effect(self):
		self.planet.research.tech_levels["Scout"] += 1

class ResearchFighter(ResearchBase):

	def __init__(self, planet):
		super().__init__(planet, "Upgrade Fighters", 50)

	def change_to():
		super().change_to()
		self.cost = 50 * (self.planet.research.tech_levels["Fighter"] + 1)

	def effect(self):
		self.planet.research.tech_levels["Fighter"] += 1

class ResearchFrigate(ResearchBase):

	def __init__(self, planet):
		super().__init__(planet, "Upgrade Frigates", 50)

	def change_to():
		super().change_to()
		self.cost = 50 * (self.planet.research.tech_levels["Frigate"] + 1)

	def effect(self):
		self.planet.research.tech_levels["Frigate"] += 1

class ResearchDestroyer(ResearchBase):

	def __init__(self, planet):
		super().__init__(planet, "Upgrade Destroyers", 50)

	def change_to():
		super().change_to()
		self.cost = 50 * (self.planet.research.tech_levels["Destroyer"] + 1)

	def effect(self):
		self.planet.research.tech_levels["Destroyer"] += 1

class ResearchColony(ResearchBase):

	def __init__(self, planet):
		super().__init__(planet, "Upgrade Colony Ships", 50)

	def change_to():
		super().change_to()
		self.cost = 50 * (self.planet.research.tech_levels["Colony"] + 1)

	def effect(self):
		self.planet.research.tech_levels["Colony"] += 1
