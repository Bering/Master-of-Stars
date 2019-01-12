from planet import Planet
import pygame

class Star:

	def __init__(self, name):
		self.name = name
		self.planets = []
		self.surface = pygame.image.load("images/star.png").convert()
		self.position = (0, 0)

	def add_planet(self):
		p = Planet(self)
		self.planets.append(p)
