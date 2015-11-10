from objects.Interpreter import Interpreter

class RequestHandler(object):
    def __init__(self,streamer,content_manager):
        self.interpreter = Interpreter(streamer,content_manager)

    def parse(self, line):
        '''Master method; figures out what was typed by the user'''
        data = line.split(' ',1)

        # Default content to empty string
        if len(data) == 1:
            data.append("")
        self.send_to_interpreter(data)


    def send_to_interpreter(self, data):
        # Get the correct method and invoke it
        method_type = 'typed_{0}'.format(data[0].lower())
        if hasattr(self.interpreter,method_type):
            method = getattr(self.interpreter,method_type)
            method(data[1])
