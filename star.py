from planet import Planet
import pygame

class Star:

	def __init__(self, name, x, y):
		self.name = name
		self.planets = []
		self.surface = pygame.image.load("images/star.png").convert()
		self.x = x
		self.y = y

	def add_planet(self, x, y):
		p = Planet(self, x, y)
		self.planets.append(p)
