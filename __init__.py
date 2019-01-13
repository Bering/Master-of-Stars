"""
Stars

Bunch of modules and classes that I made to learn Python.

Might end up being some kind of game some day.
"""

import config
from world import World
from player import Player
from ai import AI
from screen_stars import StarsScreen
from screen_planets import PlanetsScreen
from screen_quit import QuitScreen
import pygame

class Application:

	def __init__(self):
		pygame.init()
		self._surface = pygame.display.set_mode((config.window_width, config.window_height))

		self.screens = {
			"Stars" : StarsScreen(self),
			"Planets" : PlanetsScreen(self),
			"Quit" : QuitScreen(self)
		}
		self._previous_screen = None
		self._current_screen = self.screens["Quit"]
		self.change_screen(self.screens["Stars"])

		self.players = []
		for n in range(config.nb_players):
			self.players.append(Player("Player " + str(n+1)))
		self.local_player = self.players[0]
		
		self.ais = []
		for n in range(config.nb_ais):
			self.ais.append(AI("AI " + str(n+1)))
		
		self._world = World(config, self.players, self.ais)

	def print_players(self):
		print("\nGame has " + str(len(self.players)) + " player(s) and " + str(len(self.ais)) + " AI(s)")
		for p in self.players:
			print("- " + p.name + " (" + p.planets[0].name + ")")
		for ai in self.ais:
			print("- " + ai.name + " (" + ai.planets[0].name + ")")

	def print_world(self):
		print("\nCreated world with " + str(len(self._world.stars)) + " stars:")
		for s in self._world.stars:
			print("* " + s.name)
			for p in s.planets:
				print("  o " + p.name + " (" + p.size + " " + p.type + ")")

	def run(self):
		self.quit = False
		while(not self.quit):
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					self.change_screen(self.screens["Quit"])
				else:
					self._current_screen.on_event(event)

			self._current_screen.update(self._world)

			self._surface.fill((0, 0, 0))
			self._current_screen.render(self._world, self._surface)
			pygame.display.flip()

	def change_screen(self, screen):
		if (screen == self._current_screen): return

		self._previous_screen = self._current_screen
		self._current_screen = screen

	def change_screen_back(self):
		self.change_screen(self._previous_screen)

	def on_quit(self):
		self.quit = True

	def on_select_star(self, star):
		self.change_screen(self.screens["Stars"])
		self.local_player.select_star(star)

	def on_next_planet(self):
		self.change_screen(self.screens["Planets"])
		self.local_player.next_planet()

	def on_prev_planet(self):
		self.change_screen(self.screens["Planets"])
		self.local_player.prev_planet()

print("Stars v.alpha0")
app = Application()
app.print_world()
app.print_players()	
app.run()
