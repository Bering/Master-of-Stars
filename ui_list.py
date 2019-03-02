import os
import pygame
from text_renderer import TextRenderer

class UIListItem:
	def __init__(self, surface, obj, highlighted):
		self.surface = surface
		self.rect = self.surface.get_rect()
		self.object = obj
		self.highlighted = highlighted

# TODO: add a center parameter? Then we could use either position or center to place the list
class UIList:
	def __init__(self, items, position):
		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 16)
		text_renderer = TextRenderer(font)

		self.items = items
		self.buttons = []
		self.selected_index = None

		width = 0
		for item in items:
			b = UIListItem(
				text_renderer.render(item, True, (255,255,255)),
				item,
				False
			)
			self.buttons.append(b)
			width = max(width, b.rect.width)

		padding = 16
		for b in self.buttons:
			text_surface = b.surface.copy()
			b.surface = pygame.Surface((width + padding, b.rect.height + padding))
			b.surface.blit(text_surface, b.rect)
			b.rect = b.surface.get_rect()
			pygame.draw.rect(b.surface, (255,255,255), b.rect, 2)

		height = 0
		for n in range(len(self.buttons)):
			height += self.buttons[n].rect.height
			if n == 0:
				self.buttons[n].rect.center = position
			else:
				self.buttons[n].rect.topleft = self.buttons[n-1].rect.bottomleft

		self.rect = pygame.Rect((0, 0), (width, height))
		self.rect.center = position

#		self.surface = pygame.Surface((width + padding, height + 1))
#		self.rect = self.surface.get_rect()
#		self.rect.center = position
#		pygame.draw.rect(self.surface, (255,0,0), self.rect, 2)

#		for button in self.buttons:
#			button.rect.move_ip(padding / 2, padding / 2)
#			button.rect.width = width
#			self.surface.blit(button.surface, button.rect)
#			button.rect.inflate_ip(padding, padding)
#			pygame.draw.rect(self.surface, (255,255,255), button.rect, 2)
#			self.surface.blit(button.surface, button.rect)

	def handle_click(self, event):
		for n in range(len(self.buttons)):
			if self.buttons[n].rect.collidepoint(event.pos):
				self.selected_index = n
				return n
		return None

	def render(self, surface):
		for button in self.buttons:
			surface.blit(button.surface, button.rect)
		pygame.draw.rect(surface, (255,0,0), self.rect, 2)
