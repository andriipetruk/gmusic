import readline
from objects.RequestHandler import RequestHandler
from objects.ContentManager import ContentManager
from objects.CursedMenu import CursedMenu

class Interface(object):
	'''This is the command line interface. It handles all user input and sends to the processor as necessary'''
	def __init__(self):
		self.content_manager = ContentManager()
		self.display = CursedMenu(self.content_manager)

	# Waits for input from the user, then sends it off to be handled
	def __running__(self):
		'''Our default running loop which governs the UI'''
		self.content_manager.load()
		self.display.show()
