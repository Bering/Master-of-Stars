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

SCREEN_STARS = 1
SCREEN_PLANETS = 2

class Application:

	def __init__(self):
		pygame.init()
		self._surface = pygame.display.set_mode((config.window_width, config.window_height))
		self._screen = SCREEN_STARS

		self.players = []
		for n in range(config.nb_players):
			self.players.append(Player("Player " + str(n+1)))
		self._local_player = self.players[0]
		
		self.ais = []
		for n in range(config.nb_ais):
			self.ais.append(AI("AI " + str(n+1)))
		
		self.world = World(config, self.players, self.ais)


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

	def run(self):
		self._quit = False
		while(not self._quit):
			self._events()
			self._update()
			self._render()

	def _events(self):
		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				self._on_quit()
			elif (event.type == pygame.KEYUP):
				if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
					self._on_quit()
				elif (event.key == pygame.K_s):
					self._screen = SCREEN_STARS
				elif (event.key == pygame.K_PERIOD):
					self._on_next_planet()
				elif (event.key == pygame.K_p):
					if (pygame.key.get_mods() & pygame.KMOD_LSHIFT):
						self._on_prev_planet()
					elif (pygame.key.get_mods() & pygame.KMOD_RSHIFT):
						self._on_prev_planet()
					else:
						self._on_next_planet()
				elif (event.key == pygame.K_COMMA):
					self._on_prev_planet()

	def _update(self):
		pass

	def _render(self):
		self._surface.fill((0, 0, 0))
		
		if (self._screen == SCREEN_STARS):
			for s in self.world.stars:
				self._surface.blit(s.surface, s.position)
			# TODO: draw the selection marker around the selected star
		elif (self._screen == SCREEN_PLANETS):
			# TODO: draw the star in the middle
			for p in self._local_player.selected_star.planets:
				self._surface.blit(p.surface, p.position)

		pygame.display.flip()

	def _on_quit(self):
		# TODO: Are you sure?
		self._quit = True

	def _on_next_planet(self):
		self._screen = SCREEN_PLANETS
		self._local_player.next_planet()

	def _on_prev_planet(self):
		self._screen = SCREEN_PLANETS
		self._local_player.prev_planet()

print("Stars v.alpha0")
app = Application()
app.print_world()
app.print_players()	
app.run()
