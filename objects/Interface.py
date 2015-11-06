import readline
from objects.Parser import Parser
from objects.Display import Display

class Interface(object):
	'''This is the command line interface. It handles all user input and sends to the processor as necessary'''
	def __init__(self,streamer):
		self.display = Display()
		self.parser = Parser(streamer, self.display)
		readline.parse_and_bind('tab: complete')

	# Waits for input from the user, then sends it off to be handled
	def __running__(self):
		'''Our default running loop which governs the UI'''
		self.display.clear()
		self.display.help()
		while True:
			self.display.redraw()
			cmd = self.display.get_input(">  ")
			self.parser.parse(cmd)
