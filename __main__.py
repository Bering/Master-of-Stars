"""
Stars

Bunch of modules and classes that I made to learn Python.

Starting to look like a 4x game!
"""

import config
from world import World
from player import Player
from ai import AI
import screens
import pygame

class Application:

	def __init__(self):
		pygame.init()
		pygame.display.set_icon(pygame.image.load("images/star1.png"))
		pygame.display.set_caption("STARS Alpha 0.1")
		self._surface = pygame.display.set_mode((config.window_width, config.window_height))

		self.players = []
		self.local_player = Player("Player One", (0, 128, 0))
		self.players.append(self.local_player)

		for n in range(1, config.nb_players - 1):
			self.players.append(Player("Player " + str(n+1)))
		
		self.ais = []
		for n in range(config.nb_ais):
			self.ais.append(AI("AI " + str(n+1)))
		
		self.world = World(config, self.players, self.ais)

		self.screens = screens.ScreensManager(self)
		
		p = self.local_player.planets[0]
		s = self.screens.change_to("Galaxy")
		s.select_star(p.star)
		s = self.screens.change_to("Star")
		s.setup(p.star)
		s.select_planet(p)
		s = self.screens.change_to("Planet")
		s.setup(p)

	def print_world(self):
		planet_count = 0
		output = "\n"
		for s in self.world.stars:
			output += "* " + s.name + "\n"
			for p in s.planets:
				planet_count += 1
				output += "  o " + p.name + " (" + p.size + " " + p.type + ")\n"

		print(
			"\nCreated world with",
			str(len(self.world.stars)),
			"stars and",
			str(planet_count),
			"planets:",
			output
		)

	def print_players(self):
		print("Game has " + str(len(self.players)) + " player(s) and " + str(len(self.ais)) + " AI(s)")
		for p in self.players:
			print("- " + p.name + " (" + p.planets[0].name + ")")
		for ai in self.ais:
			print("- " + ai.name + " (" + ai.planets[0].name + ")")
		print("")

	def run(self):
		self.quit = False
		self.clock = pygame.time.Clock()

		while(not self.quit):
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					self.screens.change_to("Quit")
				else:
					self.screens.on_event(event)

			self.clock.tick(config.max_fps)
			self.screens.update(self.clock.get_time())

			self._surface.fill((0, 0, 0))
			self.screens.render(self._surface)
			pygame.display.flip()

	def next_turn(self):
		self.world.next_turn()
		
		for player in self.players + self.ais:
			for fleet in player.fleets:
				fleet.next_turn()

	def on_quit(self):
		self.quit = True

print("Stars v.alpha0")
app = Application()
app.print_world()
app.print_players()	
app.run()
