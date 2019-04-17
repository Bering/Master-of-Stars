from ui_text_renderer import UITextRenderer
import pygame

default_color = (255,255,255)
default_background = None
default_padding = (12,12)
default_border_size = 2
default_border_color = (255,255,255)

class UITileRenderer:

	def __init__(self, text_renderer):
		self.text_renderer = text_renderer

	def render(
		self,
		text,
		color=default_color,
		background=default_background,
		padding=default_padding,
		border_size=default_border_size,
		border_color=default_border_color
	):
		text_surface = self.text_renderer.render(text, True, color, background)
		text_rect = text_surface.get_rect()

		self.rect = text_rect.inflate(padding)
		self.surface = pygame.surface.Surface(self.rect.size)
		self.rect = self.surface.get_rect()

		if background:
			self.surface.fill(background)

		text_rect.center = self.rect.center
		self.surface.blit(text_surface, text_rect)

		pygame.draw.rect(self.surface, border_color, self.rect, border_size)
		p1 = self.rect.bottomleft[0] + 2, self.rect.bottomleft[1] - 2
		p2 = self.rect.bottomright[0] - 2, self.rect.bottomright[1] - 2
		p3 = self.rect.topright[0] - 2, self.rect.topright[1] + 2
		pygame.draw.lines(self.surface, border_color, False, [p1, p2, p3], 2)

		return self.surface
