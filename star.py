from planet import Planet
import pygame
import os

class Star:

	def __init__(self, name, x, y):
		self.name = name
		self.planets = []

		image_file = os.path.join("images", "star.png")
		self.surface = pygame.image.load(image_file).convert_alpha()
		self.rect = self.surface.get_rect().move(x, y)

		font = pygame.font.Font(None, 18)
		self.name_surf = font.render(self.name, True, (255,255,255))
		self.name_rect = self.name_surf.get_rect()
		self.name_rect.midtop = self.rect.midbottom

	def add_planet(self, x, y):
		p = Planet(self, x, y)
		self.planets.append(p)
