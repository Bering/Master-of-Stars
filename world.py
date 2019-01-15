import random
from star import Star
from star_names_stack import StarNamesStack

class World:

	def __init__(self, config, players, ais):
		self._star_names = StarNamesStack()
		self.stars = []
		for n in range(config.nb_stars):
			star = Star(
				self._star_names.pop(),
				random.randrange(config.window_width - 16),
				random.randrange(config.window_height - 16)
			)
			self.stars.append(star)

			nb_planets = random.randrange(
				config.min_planets_per_star,
				config.max_planets_per_star + 1)
			for n in range(nb_planets):
				star.add_planet(
					random.randrange(config.window_width - 16),
					random.randrange(config.window_height - 16)
				)

			self._scatter_planets(config, star)
			self._scatter_planets(config, star)

		self._scatter_stars(config)
		self._scatter_stars(config)

		for p in players:
			colony = self._colonize_random_planet(p)

		for ai in ais:
			colony = self._colonize_random_planet(ai)

	def _scatter_planets(self, config, star):
		for p in star.planets:
			for o in star.planets:
				if (o == p): continue

				if (abs(p.rect.x - o.rect.x) + abs(p.rect.y - o.rect.y) < 32):

					if (p.rect.x < o.rect.x):
						if (p.rect.x > 32):
							p.rect.move_ip(-32, 0)
							p.name_rect.move_ip(-32, 0)
						else:
							p.rect.move_ip(64, 0)
							p.name_rect.move_ip(64, 0)
					else:
						if (p.rect.x < config.window_width - 16):
							p.rect.move_ip(32, 0)
							p.name_rect.move_ip(32, 0)
						else:
							p.rect.move_ip(-64, 0)
							p.name_rect.move_ip(-64, 0)

	def _scatter_stars(self, config):
		for s in self.stars:
			for o in self.stars:
				if (o == s): continue

				if (abs(s.rect.x - o.rect.x) + abs(s.rect.y - o.rect.y) < 32):

					if (s.rect.x < o.rect.x):
						if (s.rect.x > 32):
							s.rect.move_ip(-32, 0)
							s.name_rect.move_ip(-32, 0)
						else:
							s.rect.move_ip(64, 0)
							s.name_rect.move_ip(64, 0)
					else:
						if (s.rect.x < config.window_width - 16):
							s.rect.move_ip(32, 0)
							s.name_rect.move_ip(32, 0)
						else:
							s.rect.move_ip(-64, 0)
							s.name_rect.move_ip(-64, 0)

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
