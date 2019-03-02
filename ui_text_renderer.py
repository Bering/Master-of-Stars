import pygame

""" Text renderer that can render multiple lines of text separated by '\n'"""
class UITextRenderer:

	def __init__(self, font):
		self.font = font

	def render(self, text, antialias, color, background=None):
		"""Same parameters than the Font.render() function"""

		width = 0
		line_count = 0
		lines = text.splitlines()
		for line in lines:
			size = self.font.size(line)
			width = max(width, size[0])
			line_count += 1

		y = 0
		line_size = self.font.get_linesize()
		text_surface = pygame.surface.Surface((width, line_count * line_size))

		if background:
			text_surface.fill(background)

		for line in lines:
			line_surface = self.font.render(line, antialias, color, background)
			line_rect = line_surface.get_rect().move(0, y)
			text_surface.blit(line_surface, line_rect)
			y += line_size

		return text_surface
