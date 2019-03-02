import os
import pygame
from ui_text_renderer import UITextRenderer
from ui_tile_renderer import UITileRenderer

class UIPopupButton:
	def __init__(self, surface):
		self.surface = surface
		self.rect = self.surface.get_rect()

class UIPopup:	
	def __init__(self, options, position):
		filename = os.path.join("fonts", "OpenSansRegular.ttf")
		font = pygame.font.Font(filename, 14)
		text_renderer = UITextRenderer(font)
		tile_renderer = UITileRenderer(text_renderer)

		self.options = options
		self.buttons = []
		for n in range(len(options)):
			self.buttons.append(UIPopupButton(tile_renderer.render(options[n].name)))
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
