from gmusic.core.Controller import Controller

class RequestHandler(object):
    """Class which is responsible for decoding user input"""

    def __init__(self, content_manager):
        self.controller = Controller(content_manager)

    def parse(self, line):
        '''Master method; figures out what was typed by the user'''
        data = line.split(' ', 1)

        # Default content to empty string
        if len(data) == 1:
            data.append("")
        self.send_to_controller(data)


    def send_to_controller(self, data):
        """Get the correct method and invoke it"""
        method_type = 'typed_{0}'.format(data[0].lower())
        if hasattr(self.controller, method_type):
            method = getattr(self.controller, method_type)
            method(data[1])
