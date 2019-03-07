from screen_galaxy import GalaxyScreen
from screen_star import StarScreen
from screen_planet import PlanetScreen
from screen_production import ProductionScreen
from screen_research import ResearchScreen
from screen_fleets import FleetsScreen
from screen_test import TestScreen
from screen_quit import QuitScreen

class ScreensManager:

	def __init__(self, app):
		self.screens = {
			"Galaxy" : GalaxyScreen(app),
			"Star" : StarScreen(app),
			"Planet" : PlanetScreen(app),
			"Production" : ProductionScreen(app),
			"Research" : ResearchScreen(app),
			"Fleet" : FleetsScreen(app),
			"Test" : TestScreen(app),
			"Quit" : QuitScreen(app)
		}
		self._previous_screen_name = "None"
		self._current_screen_name = "None"

	def change_to(self, screen_name):
		if screen_name not in self.screens:
			raise KeyError("Invalid screen name: " + screen_name)

		self._previous_screen_name = self._current_screen_name
		self._current_screen_name = screen_name
		self._current_screen = self.screens[screen_name]
		return self._current_screen

	def change_back(self):
		self.change_to(self._previous_screen_name)
		return self._current_screen

	def on_event(self, event):
		self._current_screen.on_event(event)

	def update(self, delta_time):
		self._current_screen.update(delta_time)

	def render(self, surface):
		self._current_screen.render(surface)