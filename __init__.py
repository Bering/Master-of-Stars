"""
Stars

Bunch of modules and classes that I made to learn Python.

Might end up being some kind of game some day.
"""

import config
from world import World
from player import Player
from ai import AI
import pygame

class Application:

	def __init__(self):
		self.players = []
		for n in range(config.nb_players):
			self.players.append(Player("Player " + str(n+1)))
		
		self.ais = []
		for n in range(config.nb_ais):
			self.ais.append(AI("AI " + str(n+1)))
		
		self.world = World(config, self.players, self.ais)

		pygame.init()
		self.screen = pygame.display.set_mode((640, 480))

	def print_players(self):
		print("\nGame has " + str(len(self.players)) + " player(s) and " + str(len(self.ais)) + " AI(s)")
		for p in self.players:
			print("- " + p.name + " (" + p.planets[0].name + ")")
		for ai in self.ais:
			print("- " + ai.name + " (" + ai.planets[0].name + ")")

	def print_world(self):
		print("\nCreated world with " + str(len(self.world.stars)) + " stars:")
		for s in self.world.stars:
			print("* " + s.name)
			for p in s.planets:
				print("  o " + p.name + " (" + p.size + " " + p.type + ")")

	def loop(self):
		while(1):
			for event in pygame.event.get():
				if (event.type == pygame.QUIT):
					return

print("Stars v.alpha0")
app = Application()
app.print_world()
app.print_players()	
app.loop()
