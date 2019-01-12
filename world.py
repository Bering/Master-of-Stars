import random
from star import Star
from star_names_stack import StarNamesStack

class World:

	def __init__(self, config, players, ais):
		self._star_names = StarNamesStack()
		self.stars = []
		for n in range(config.nb_stars):
			star = Star(self._star_names.pop())
			self.stars.append(star)

			nb_planets = random.randrange(
				config.min_planets_per_star,
				config.max_planets_per_star + 1)
			for n in range(nb_planets):
				star.add_planet()

		for p in players:
			colony = self._colonize_random_planet(p)
			p.select_star(colony.star)
			p.select_planet(colony)

		for ai in ais:
			colony = self._colonize_random_planet(ai)
			p.select_star(colony.star)
			p.select_planet(colony)

	def _colonize_random_planet(self, player):
		owner = player
		while(owner is not None):
			star = self.stars[random.randrange(len(self.stars))]
			planet = star.planets[random.randrange(len(star.planets))]
			owner = planet.player
		
		player.colonize_planet(planet)
		planet.defense = 5
		return planet

	def next_turn(self):
		for s in self.stars:
			for p in s.planets:
				p.next_turn()
