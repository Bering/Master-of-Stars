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
SCREEN_QUIT = 99

class Application:

	def __init__(self):
		pygame.init()
		self._surface = pygame.display.set_mode((config.window_width, config.window_height))
		self._previous_screen = SCREEN_STARS
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
				self._on_close()
			elif (event.type == pygame.KEYUP):
				if (self._screen == SCREEN_STARS) or (self._screen == SCREEN_PLANETS):
					if (event.key == pygame.K_q) or (event.key == pygame.K_ESCAPE):
						self._on_close()
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
				else:
					if (event.key == pygame.K_y):
						self._on_quit()
					elif (event.key == pygame.K_n):
						self._screen = self._previous_screen

	def _update(self):
		pass

	def _render(self):
		self._surface.fill((0, 0, 0))
		
		if (self._screen == SCREEN_STARS):
			for s in self.world.stars:
				self._surface.blit(s.surface, (s.x, s.y))
			# TODO: draw the selection marker around the selected star
		elif (self._screen == SCREEN_PLANETS):
			s = self._local_player.selected_star
			rect = s.surface.get_rect()
			rect.center = self._surface.get_rect().center
			self._surface.blit(s.surface, rect)
			for p in s.planets:
				self._surface.blit(p.surface, (p.x, p.y))
		elif (self._screen == SCREEN_QUIT):
			font = pygame.font.Font(None, 24)
			text_surf = font.render("Are you sure?", True, (255,255,255))
			rect = text_surf.get_rect()
			rect.center = self._surface.get_rect().center
			self._surface.blit(text_surf, rect)

			rect.x -= 15
			rect.y -= 15
			rect.width += 30
			rect.height += 30
			pygame.draw.rect(self._surface, (255,255,255), rect, 2)

		pygame.display.flip()

	def _on_close(self):
		self._previous_screen = self._screen
		self._screen = SCREEN_QUIT

	def _on_quit(self):
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
