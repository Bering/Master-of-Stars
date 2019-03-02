import os
import pygame
from text_renderer import TextRenderer

default_color = (255, 255, 255)
default_highlight_color = (48, 48, 48)

class UIListItem:
	def __init__(self, surface, obj, highlighted):
		self.surface = surface
		self.rect = self.surface.get_rect()
		self.object = obj
		self.is_highlighted = highlighted

# TODO: add a center parameter? Then we could use either position or center to place the list
class UIList:
	def __init__(self, items, position, color=default_color, highlight_color=default_highlight_color):
		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 16)
		text_renderer = TextRenderer(font)

		self.items = items
		self.buttons = []
		self.selected_index = None

		width = 0
		for item in items:
			b = UIListItem(
				text_renderer.render(item, True, color),
				item,
				False
			)
			b.surface_highlighted = text_renderer.render(
				item,
				True,
				color,
				highlight_color
			)
			self.buttons.append(b)
			width = max(width, b.rect.width)

		padding = 16
		for b in self.buttons:
			text_surface = b.surface.copy()
			text_surface_h = b.surface_highlighted.copy()
			b.surface = pygame.Surface((width + padding, b.rect.height + padding))
			b.surface_highlighted = b.surface.copy()
			b.surface_highlighted.fill(highlight_color)
			b.rect.move_ip(padding/2, padding/2)
			b.surface.blit(text_surface, b.rect)
			b.surface_highlighted.blit(text_surface_h, b.rect)
			b.rect = b.surface.get_rect()
			pygame.draw.rect(b.surface, color, b.rect, 2)
			pygame.draw.rect(b.surface_highlighted, color, b.rect, 2)

		height = 0
		for n in range(len(self.buttons)):
			height += self.buttons[n].rect.height
			if n > 0:
				self.buttons[n].rect.topleft = self.buttons[n-1].rect.bottomleft
				self.buttons[n].rect.y -= 1

		self.rect = pygame.Rect((0, 0), (width + padding, height - (len(self.buttons) - 1)))
		self.rect.center = position

	def handle_click(self, event):
		for n in range(len(self.buttons)):
			if self.buttons[n].rect.collidepoint(event.pos):
				self.select(n)
				return n
		return None

	def select(self, index):
		self.selected_index = index
		for n in range(len(self.buttons)):
			self.buttons[n].is_highlighted = (index == n)

	def render(self, surface):
		delta_x = self.rect.topleft[0] - self.buttons[0].rect.x
		delta_y = self.rect.topleft[1] - self.buttons[0].rect.y
		for button in self.buttons:
			if delta_x != 0 or delta_y != 0:
				button.rect.move_ip(delta_x, delta_y)
			if button.is_highlighted:
				surface.blit(button.surface_highlighted, button.rect)
			else:
				surface.blit(button.surface, button.rect)
