class Player:
	def __init__(self, name):
		self.name = name
		self.fleets = []

class Fleet:
	def __init__(self, player, name):
		self.player = player
		self.name = name

class Planet:
	def __init__(self, player, name):
		self.player = player
		self.name = name
		self.fleets = []

players = [
	Player("Player One"),
	Player("AI 1"),
	Player("AI 2"),
	Player("AI 3")
]

class Game:
	def __init__(self):
		fleet1 = Fleet(players[0], "1st Fleet")
		fleet2 = Fleet(players[1], "1st Fleet")
		fleet3 = Fleet(players[2], "1st Fleet")
		fleet4 = Fleet(players[0], "2nd Fleet")

		players[0].fleets.append(fleet1)
		players[0].fleets.append(fleet4)
		players[1].fleets.append(fleet2)
		players[2].fleets.append(fleet3)

		planet = Planet(players[1], "Somewhere")

		print("Test 1: ", end="")
		planet.fleets.clear()
		planet.fleets.append(fleet1)
		f1, f2, f3 = self.fleet_picker(players[0], planet.fleets)
		if f1 == fleet1 and f2 == None and f3 == None:
			print("Success")
		else:
			print("Fail")

		print("Test 2: ", end="")
		planet.fleets.clear()
		planet.fleets.append(fleet1)
		planet.fleets.append(fleet2)
		planet.fleets.append(fleet3)
		f1, f2, f3 = self.fleet_picker(players[0], planet.fleets)
		if f1 == fleet1 and f2 == fleet2 and f3 == fleet3:
			print("Success")
		else:
			print("Fail")

		print("Test 3: ", end="")
		planet.fleets.clear()
		planet.fleets.append(fleet1)
		planet.fleets.append(fleet2)
		planet.fleets.append(fleet4)
		f1, f2, f3 = self.fleet_picker(players[0], planet.fleets)
		if f1 == fleet1 and f2 == fleet2 and f3 == None: # fleet4 not chosen since only one fleet per player
			print("Success")
		else:
			print("Fail")

		print("Test 4: ", end="")
		planet.fleets.clear()
		planet.fleets.append(fleet1)
		planet.fleets.append(fleet2)
		planet.fleets.append(fleet3)
		planet.fleets.append(fleet4)
		f1, f2, f3 = self.fleet_picker(players[0], planet.fleets)
		if f1 == fleet1 and f2 == fleet2 and f3 == fleet3: # fleet4 not chosen since there are 3 players
			print("Success")
		else:
			print("Fail")

	# 3 fleets to choose
	# if local player has a fleet, it must be f1
	# only choose the first fleet of every per player
	# if more than 3 players, only choose the first 3
	def fleet_picker(self, local_player, fleets):
		f1 = None
		f2 = None
		f3 = None
		player_fleets = {}

		# First fleet of every player
		for f in fleets:
			if f.player not in player_fleets:
				player_fleets[f.player] = f

		# if local player has a fleet, it is f1
		if local_player in player_fleets:
			f1 = player_fleets[local_player]
			del player_fleets[local_player]

		for player, fleet in player_fleets.items():
			if not f1:
				f1 = player_fleets[player]
			elif not f2:
				f2 = player_fleets[player]
			elif not f3:
				f3 = player_fleets[player]
			else:
				break

		return f1, f2, f3

g = Game()
