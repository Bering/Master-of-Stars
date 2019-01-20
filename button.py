import pygame

default_font_name = None
default_font_size = 24
default_color = (255, 255, 255)
default_background = (64, 64, 64)
default_border_color = (255,255,255)
default_padding = (12, 12)

# TODO: tooltips

class Button:

	def __init__(
		self,
		label,
		on_click,
		font_name=default_font_name,
		font_size=default_font_size,
		color=default_color,
		background=default_background,
		color_border=default_border_color,
		padding=default_padding
	):
		self.padding = padding
		self.on_click = on_click

		font = pygame.font.Font(font_name, font_size)
		surface = font.render(label, True, color, background)
		rect = surface.get_rect()

		self.rect = rect.inflate(padding)
		self.surface = pygame.Surface(self.rect.size, flags=surface.get_flags())
		self.surface.fill(background)

		self.rect = self.surface.get_rect()
		rect.center = self.rect.center
		self.surface.blit(surface, rect)
		pygame.draw.rect(self.surface, color_border, self.rect, 2)

		p1 = self.rect.bottomleft[0] + 2, self.rect.bottomleft[1] - 2
		p2 = self.rect.bottomright[0] - 2, self.rect.bottomright[1] - 2
		p3 = self.rect.topright[0] - 2, self.rect.topright[1] + 2
		pygame.draw.lines(self.surface, color_border, False, [p1, p2, p3], 2)

	def render(self, surface):
		surface.blit(self.surface, self.rect)
