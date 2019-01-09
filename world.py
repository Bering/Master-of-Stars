import random
from star import Star
from star_names_stack import StarNamesStack

class World:

	star_names = StarNamesStack()

	def __init__(self, config):
		self.stars = []
		for n in range(0, config.nb_stars):
			star = Star(self.star_names.pop())
			self.stars.append(star)

			nb_planets = random.randrange(
				config.min_planets_per_star,
				config.max_planets_per_star + 1)
			for n in range(0, nb_planets):
				star.add_planet()
