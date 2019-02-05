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
		self.destination_center_star_rect = None
		
		image_file = os.path.join("images", "fleet.png")
		self.surface = pygame.image.load(image_file).convert_alpha()

		# rect in the galaxy screen
		self.rect = self.surface.get_rect()
		star_rect = planet.star.rect
		self.rect.midleft = star_rect.topright

		# rect in the star screen
		self.rect_s = planet.rect.copy()
		self.rect_s.midleft = planet.rect.topright

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
		"""Move between stars in the galaxy screen"""
		if self.destination_star:
			if not self.star:
				# Cannot change destination while moving
				return
			elif self.star == star:
				# But can cancel departure
				self.destination_star = star
				self.arrive()
				return

		self.destination_star = star

		delta_x = self.destination_star.rect.center[0] - self.star.rect.center[0]
		delta_y = self.destination_star.rect.center[1] - self.star.rect.center[1]

		heading = math.atan2(delta_x, delta_y)

		self.rect.center = self.star.rect.center
		self.rect.move_ip(math.sin(heading) * 16, math.cos(heading) * 16)

	def set_destination_center_star(self, star_rect):
		"""Go to the star from a planet in the star screen"""
		#if self.destination_planet:
		#	if not self.planet:
		#		# Cannot change destination while moving
		#		return
		#	elif self.planet == planet:
		#		# But can cancel departure
		#		self.destination_planet = planet
		#		self.arrive()
		#		return

		self.destination_center_star_rect = star_rect

		delta_x = star_rect.center[0] - self.planet.rect.center[0]
		delta_y = star_rect.center[1] - self.planet.rect.center[1]

		heading = math.atan2(delta_x, delta_y)

		self.rect_s.center = self.planet.rect.center
		self.rect_s.move_ip(
			math.sin(heading) * self.planet.rect.width,
			math.cos(heading) * self.planet.rect.height
		)

	def set_destination_planet(self, source_rect, planet):
		"""Move between planets and from a planet to the star in the Star Screen"""
		if self.destination_planet:
			if not self.planet:
				# Cannot change destination while moving
				return
			elif self.planet == planet:
				# But can cancel departure
				self.destination_planet = planet
				self.arrive()
				return

		self.destination_planet = planet

		delta_x = planet.rect.center[0] - source_rect.center[0]
		delta_y = planet.rect.center[1] - source_rect.center[1]

		heading = math.atan2(delta_x, delta_y)

		self.rect_s.center = source_rect.center
		self.rect_s.move_ip(math.sin(heading) * source_rect.width, math.cos(heading) * source_rect.height)

	def arrive(self):
		if self.destination_star:
			self.rect.midleft = self.destination_star.rect.topright
			self.star = self.destination_star
			self.star.fleets.append(self)
			self.destination_star = None
			return

		if self.destination_planet:
			self.planet = self.destination_planet
			self.planet.fleets.append(self)
			self.rect_s.midleft = self.planet.rect.topright
			self.destination_planet = None
			return

		if self.destination_center_star_rect:
			self.rect_s.midleft = self.destination_center_star_rect.topright
			self.destination_center_star_rect = None
			return

	def next_turn(self):
		if not self.destination_star and not self.destination_planet and not self.destination_center_star_rect:
			return

		if self.destination_star and self.star:
			self.star.fleets.remove(self)
			self.star = None

		if self.planet:
			self.planet.fleets.remove(self)
			self.planet = None

		if self.destination_planet or self.destination_center_star_rect:
			self.arrive()
			return

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
