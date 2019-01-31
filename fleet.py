from ship import Ship
import os
import math
import pygame

class Fleet:

	def __init__(self, planet, number):
		self.name = self.generate_name(number)
		self.star = planet.star
		self.star.fleets.append(self)
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

	def set_destination_star(self, star):
		self.destination_star = star
		self.planet.fleets.remove(self)
		self.planet = None

		# NOTE: This codes is assuming the fleet is in orbit around a star

		delta_x = self.destination_star.rect.x - self.star.rect.x
		delta_y = self.destination_star.rect.y - self.star.rect.y

		heading = math.atan2(delta_x, delta_y)

		self.rect.center = self.star.rect.center
		self.rect.move_ip(math.sin(heading) * 16, math.cos(heading) * 16)

	def arrive(self):
		self.rect.midleft = self.destination_star.rect.topright
		self.star = self.destination_star
		self.destination_star = None
		self.star.fleets.append(self)
		
	def next_turn(self):
		if not self.destination_star:
			return

		if self.star:
			self.star.fleets.remove(self)
			self.star = None

		delta_x = self.destination_star.rect.x - self.rect.x
		delta_y = self.destination_star.rect.y - self.rect.y
		remaining_distance = math.hypot(delta_x, delta_y)

		max_speed = self.get_speed()
		distance_this_turn = min(remaining_distance, max_speed)

		heading = math.atan2(delta_x, delta_y)

		self.rect.move_ip(
			math.sin(heading) * distance_this_turn,
			math.cos(heading) * distance_this_turn
		)

		if self.rect.colliderect(self.destination_star.rect):
			self.arrive()

	def get_speed(self):
		max_speed = math.inf

		for s in self.ships:
			if s.speed < max_speed:
				max_speed = s.speed

		return max_speed
