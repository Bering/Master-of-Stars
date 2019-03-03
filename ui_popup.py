from ui_list import UIList

class UIPopup:	
	def __init__(self, options, position):
		self.options = options
		self.list_items = []
		for option in options:
			self.list_items.append(option.name)
		self.list = UIList(self.list_items, center=position, padding=12)

	def handle_click(self, event):
		for n in range(len(self.options)):
			self.list.handle_click(event)
			index = self.list.get_selected_index()
			if index == None:
				return None
			return self.options[index]

	def render(self, surface):
		self.list.render(surface)
