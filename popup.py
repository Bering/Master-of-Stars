import os
import pygame
from text_renderer import TextRenderer
from tile_renderer import TileRenderer

class PopupButton:
	def __init__(self, surface):
		self.surface = surface
		self.rect = self.surface.get_rect()

class Popup:	
	def __init__(self, options, position):
		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 14)
		text_renderer = TextRenderer(font)
		tile_renderer = TileRenderer(text_renderer)

		self.options = options
		self.buttons = []
		for n in range(len(options)):
			self.buttons.append(PopupButton(tile_renderer.render(options[n].name)))
			if n == 0:
				self.buttons[n].rect.center = position
			else:
				self.buttons[n].rect.topleft = self.buttons[n-1].rect.bottomleft
				self.buttons[n].rect.y -= 1

	def handle_click(self, event):
		for n in range(len(self.buttons)):
			if self.buttons[n].rect.collidepoint(event.pos):
				return self.options[n]
		return None

	def render(self, surface):
		for button in self.buttons:
			surface.blit(button.surface, button.rect)
