class ScreenBase:

	def __init__(self, app):
		self._app = app

	def on_event(self, event):
		pass

	def update(self):
		pass

	def render(self, surface):
		pass
