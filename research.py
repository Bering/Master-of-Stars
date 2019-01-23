class ResearchBase:

	def __init__(self, player, name, cost):
		self.player = player
		self.name = name
		self.cost = cost
		self.progress = 0

	def next_turn(self, science_units):
		self.progress += science_units

		if(self.progress >= self.cost):
			self.effect()

	def effect(self):
		pass


class ResearchShipyard2(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Shipyard", 50)

	def effect(self):
		self.player.tech_levels["Shipyard"] = 2

class ResearchShipyard3(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Shipyard", 500)

	def effect(self):
		self.player.tech_levels["Shipyard"] = 3

class ResearchScout(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Scouts", 100)

	def effect(self):
		self.player.tech_levels["Scout"] += 1
		self.cost = 50 * (self.player.tech_levels["Scout"] + 1)

class ResearchFrigate(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Frigates", 100)

	def effect(self):
		self.player.tech_levels["Frigate"] += 1
		self.cost = 50 * (self.player.tech_levels["Frigate"] + 1)

class ResearchDestroyer(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Destroyers", 1000)

	def effect(self):
		self.player.tech_levels["Destroyer"] += 1
		self.cost = 100 * (self.player.tech_levels["Destroyer"] + 1)

class ResearchColony(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Colony Ships", 1000)

	def effect(self):
		self.player.tech_levels["Colony"] += 1
		self.cost = 100 * (self.player.tech_levels["Colony"] + 1)
