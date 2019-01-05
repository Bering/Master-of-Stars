import random

class StarNamesList:

	def __init__(self):
		f = open("star_names.txt", "r")
		self.names = f.readlines()
		for item in enumerate(self.names):
			index = item[0]
			name = item[1]
			self.names[index] = name.strip()
		f.close()

	def pop(self):
		if (len(self.names) == 0): raise RuntimeError("Out of star names!")

		index = random.randrange(0, len(self.names))
		name = self.names[index]
		self.names.remove(name)
		return name
