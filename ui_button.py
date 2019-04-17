import pygame

# TODO: tooltips

class UIButton:

	def __init__(
		self,
		label,
		on_click,
		font = None,
		color = (255, 255, 255),
		background = (64, 64, 64),
		color_border = (255, 255, 255),
		padding = (12, 12)
	):
		self.label = label
		self.on_click = on_click

		if not font:
			font = pygame.font.Font(None, 24)
		text_surface = font.render(label, True, color, background)
		text_rect = text_surface.get_rect()

		self.rect = text_rect.inflate(padding)
		self.surface = pygame.Surface(self.rect.size, flags=text_surface.get_flags())
		self.rect = self.surface.get_rect()
		
		self.surface.fill(background)

		text_rect.center = self.rect.center
		self.surface.blit(text_surface, text_rect)
		
		pygame.draw.rect(self.surface, color_border, self.rect, 2)
		p1 = self.rect.bottomleft[0] + 2, self.rect.bottomleft[1] - 2
		p2 = self.rect.bottomright[0] - 2, self.rect.bottomright[1] - 2
		p3 = self.rect.topright[0] - 2, self.rect.topright[1] + 2
		pygame.draw.lines(self.surface, color_border, False, [p1, p2, p3], 2)

	def render(self, surface):
		surface.blit(self.surface, self.rect)
