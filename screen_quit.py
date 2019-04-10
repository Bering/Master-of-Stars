import pygame
from screen_base import ScreenBase
from ui_button import UIButton


class QuitScreen(ScreenBase):

	def __init__(self, app):
		super().__init__(app)
		font = pygame.font.Font(None, 24)
		self.text_surf = font.render("Are you sure?", True, (255,255,255))
		self.text_rect = self.text_surf.get_rect()

		self.yes = UIButton("Yes", self.on_yes)
		self.no = UIButton("No", self.on_no)

	def on_event(self, event):
		if (event.type == pygame.KEYUP):
			if (event.key == pygame.K_y):
				self.on_yes()
			elif (event.key == pygame.K_n):
				self.on_no()

		elif (event.type == pygame.MOUSEBUTTONUP):
			for button in [self.yes, self.no]:
				if button.rect.collidepoint(event.pos):
					button.on_click()

	def update(self, delta_time):
		pass
		
	def render(self, surface):
		self.text_rect.center = surface.get_rect().center
		surface.blit(self.text_surf, self.text_rect)
		rect = self.text_rect.inflate(30, 30)
		pygame.draw.rect(surface, (255,255,255), rect, 2)

		self.yes.rect.topright = rect.midbottom
		self.no.rect.topleft = rect.midbottom

		self.yes.rect.move_ip(-10, 10)
		self.no.rect.move_ip(10, 10)

		surface.blit(self.yes.surface, self.yes.rect)
		surface.blit(self.no.surface, self.no.rect)

	def on_yes(self):
		self._app.on_quit()

	def on_no(self):
		self._app.screens.change_back()
