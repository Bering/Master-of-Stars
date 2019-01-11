import random
from star import Star
from star_names_stack import StarNamesStack

class World:

	def __init__(self, config, players, ais):
		self._star_names = StarNamesStack()
		self.stars = []
		for n in range(0, config.nb_stars):
			star = Star(self._star_names.pop())
			self.stars.append(star)

			nb_planets = random.randrange(
				config.min_planets_per_star,
				config.max_planets_per_star + 1)
			for n in range(0, nb_planets):
				star.add_planet()

		for p in players:
			self._colonize_random_planet(p)

		for ai in ais:
			self._colonize_random_planet(ai)

	def _colonize_random_planet(self, player):
		
		owner = player
		while(owner is not None):
			star = self.stars[random.randrange(0, len(self.stars))]
			planet = star.planets[random.randrange(0, len(star.planets))]
			owner = planet.player
		
		player.colonize_planet(planet)
		planet.defense = 5

	def next_turn(self):
		for s in self.stars:
			for p in s.planets:
				p.next_turn()
	