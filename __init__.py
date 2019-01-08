import config
from world import World

print("Stars v.alpha0")

world = World(config)

print("Created world with " + str(len(world.stars)) + " stars")

for s in world.stars:
	print("* " + s.name)
	for p in s.planets:
		print("  o " + p.name + " (" + p.size + " " + p.type + ")")
