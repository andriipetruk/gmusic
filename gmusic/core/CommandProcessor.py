from gmusic.model.MenuElement import MenuElement
from gmusic.core.EventHandler import EventHandler

class CommandProcessor(EventHandler):
    """Class which is responsible for decoding user input"""
    def __init__(self, handler, content_handler, player_controller):
        EventHandler.__init__(self)
        self.attachments.append(handler)
        self.content_handler = content_handler
        self.player_controller = player_controller

    def process(self, cmd_class, cmd_args=None):
        '''Master method; figures out what was typed by the user'''
        command = self.build_type('command', cmd_class)

        if command is None:
            return

        command.player_controller = self.player_controller
        command.content_handler = self.content_handler

        # See if there is an event that needs to run pre-execution
        if hasattr(command, 'pre_execute'):
            pre_execute_event = command.pre_execute(cmd_args)
            if pre_execute_event is not None:
                self.notify_attachments(*pre_execute_event)

        # See if there is any event that needs to be run after execution
        if hasattr(command, 'execute'):
            execute_event = command.execute(cmd_args)
            if execute_event is not None:
                self.notify_attachments(*execute_event)


    def parse(self, line):
        '''Attempt to process input from command line'''
        try:
            split_results = line.strip().split(' ', 1)
        except:
            return

        cmd_args = None
        cmd_class = split_results[0]
        if len(split_results) > 1:
            cmd_args = {"query": split_results[1]}

        self.process(cmd_class.capitalize(), cmd_args)


    def build_type(self, m_type, m_class, m_args=None):
        '''Fleshes out the Event with parameters as specified'''
        module = __import__('gmusic.model.{0}s'.format(m_type.lower()))
        if not hasattr(module, m_class):
            return

        instantiated = getattr(module, m_class)(self)
        if m_args is not None:
            for param in (p for p in m_args if hasattr(instantiated, p)):
                setattr(instantiated, param, m_args[param])

        return instantiated
