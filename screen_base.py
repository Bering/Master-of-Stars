class ScreenBase:

	def __init__(self, app):
		self._app = app

	def on_event(self, event):
		pass

	def update(self, world):
		pass

	def render(self, world, surface):
		pass
