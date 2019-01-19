from ship import Ship
import os
import pygame

class Fleet:

	def __init__(self, planet, number):
		self.name = self.generate_name(number)
		self.planet = planet
		self.player = planet.player
		self.ships = []

		image_file = os.path.join("images", "fleet.png")
		self.surface = pygame.image.load(image_file).convert_alpha()
		self.rect = self.surface.get_rect().move(planet.rect.x, planet.rect.y)

		font = pygame.font.Font(None, 18)
		self.name_surf = font.render(self.name, True, (255,255,255))
		self.name_rect = self.name_surf.get_rect()
		self.name_rect.midleft = planet.rect.topright

	def generate_name(self, number):

		if number == 11: return "11th"
		if number == 12: return "12th"
		if number == 13: return "13th"

		name = str(number)
		last_char = name[-1]

		if last_char == "1": return name + "st"
		if last_char == "2": return name + "nd"
		if last_char == "3": return name + "rd"
		return name + "th"

	def create_ship(self, ship_type, tech_level):
		ship = Ship(ship_type, tech_level)
		self.ships.append(ship)
