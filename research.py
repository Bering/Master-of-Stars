class ResearchBase:

	def __init__(self, player, name, desc, cost):
		self.player = player
		self.name = name
		self.desc = desc
		self.cost = cost
		self.progress = 0
		self.is_complete = False

	def next_turn(self, science_units):

		if self.progress < self.cost:
			self.progress += science_units

			if(self.progress >= self.cost):
				self.effect()
				self.is_complete = True

	def effect(self):
		self.progress = 0


class ResearchShipyard(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Shipyard", "Allow Frigates.", 50)

	def effect(self):
		super().effect()
		self.player.tech_levels["Shipyard"] += 1
		self.desc = "Allow Colony Ships and Destroyers"
		self.cost = 500

class ResearchScout(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Upgrade Scouts", "Better Scouts", 100)

	def effect(self):
		super().effect()
		self.player.tech_levels["Scout"] += 1
		self.cost = 50 * (self.player.tech_levels["Scout"] + 1)

class ResearchFrigate(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Frigates", "Basic warships", 100)

	def effect(self):
		super().effect()
		self.player.tech_levels["Frigate"] += 1
		self.name = "Frigates Upgrades"
		self.desc = "Better Frigates"
		self.cost = 100 * (self.player.tech_levels["Frigate"] + 1)

class ResearchDestroyer(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Destroyers", "Great against Frigates", 1000)

	def effect(self):
		super().effect()
		self.player.tech_levels["Destroyer"] += 1
		self.name = "Destroyers Upgrades"
		self.desc = "Better Destroyers"
		self.cost = 1000 * (self.player.tech_levels["Destroyer"] + 1)

class ResearchColony(ResearchBase):

	def __init__(self, player):
		super().__init__(player, "Colony Ships", "Ships for colonization", 1000)

	def effect(self):
		super().effect()
		self.player.tech_levels["Colony"] += 1
		self.name = "Colony Ships Upgrades"
		self.desc = "Better Colony Ships"
		self.cost = 1000 * (self.player.tech_levels["Colony"] + 1)
