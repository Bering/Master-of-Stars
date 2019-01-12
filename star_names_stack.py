import random

class StarNamesStack:

	def __init__(self):
		f = open("star_names.txt", "r")
		self.names = f.readlines()
		f.close()
		
		for item in enumerate(self.names):
			index = item[0]
			name = item[1]
			self.names[index] = name.strip()

	def pop(self):
		if (not self.names): raise IndexError("Out of star names!")

		index = random.randrange(len(self.names))
		name = self.names[index]
		self.names.remove(name)
		return name
