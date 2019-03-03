import os
import pygame
from ui_text_renderer import UITextRenderer

default_color = (255, 255, 255)
default_highlight_color = (48, 48, 48)

class UIListItem:
	def __init__(self, surface, item, is_highlighted):
		self.surface = surface
		self.rect = self.surface.get_rect()
		self.item = item
		self.is_highlighted = is_highlighted

class UIList:
	def __init__(
		self,
		items,
		position=None,
		center=None,
		padding = 16,
		color=default_color,
		highlight_color=default_highlight_color
	):
		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 16)
		text_renderer = UITextRenderer(font)

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
		if position:
			self.rect.topleft = position
		if center:
			self.rect.center = center

	def select(self, index):
		self.selected_index = index
		for n in range(len(self.buttons)):
			self.buttons[n].is_highlighted = (index == n)

	def get_selected_index(self):
		return self.selected_index

	def get_selected_item(self):
		if self.selected_index == None:
			return None

		return self.buttons[self.selected_index].item

	def handle_click(self, event):
		for n in range(len(self.buttons)):
			if self.buttons[n].rect.collidepoint(event.pos):
				self.select(n)
				return True
		return False

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
