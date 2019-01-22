_types = ["Scout", "Frigate", "Destroyer", "Colony"]

class Ship:

	def __init__(self, ship_type, tech_level):
		if ship_type not in _types:
			raise KeyError("Invalid ship type")

		self.type = ship_type
		self.tech_level = tech_level

