from planet import Planet
import pygame
import os

class Star:

	def __init__(self, name, x, y):
		self.name = name
		self.planets = []
		self.surface = pygame.image.load(os.path.join("images", "star.png")).convert_alpha()
		self.x = x
		self.y = y

	def add_planet(self, x, y):
		p = Planet(self, x, y)
		self.planets.append(p)
