from ship import Ship
import os
import pygame

class Fleet:

	def __init__(self, planet, number):
		self.name = self.generate_name(number)
		self.star = planet.star
		self.planet = planet
		self.player = planet.player
		self.ships = []
		self.destination_star = None
		self.destination_planet = None

		image_file = os.path.join("images", "fleet.png")
		self.surface = pygame.image.load(image_file).convert_alpha()
		self.rect = self.surface.get_rect()
		star_rect = planet.star.rect
		self.rect.midleft = star_rect.topright

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

	def get_ship_counts(self):
		counts = {
			"Scout" : 0,
			"Frigate" : 0,
			"Destroyer" : 0,
			"Colony" : 0,
			"Total" : 0
		}
		for ship in self.ships:
			counts[ship.type] += 1
			counts["Total"] += 1

		return counts

	def get_best_ship(self, ship_type):
		best_ship = None

		for ship in self.ships:
			if ship.type == ship_type:
				if not best_ship:
					best_ship = ship
				if ship.tech_level > best_ship.tech_level:
					best_ship = ship

		return best_ship

	def destroy_ship(self, ship):
		self.ships.remove(ship)

	def next_turn(self):
		# TODO: Move towards destination_star
		if self.rect.colliderect(self.destination_star.rect):
			self.rect.midleft = self.destination_star.rect.topright
			self.destination_star = None

	def set_destination_star(self, star):
		self.destination_star = star
		self.rect.midright = self.star.rect.topleft
