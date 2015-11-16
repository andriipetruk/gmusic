from objects.Interface import Interface
import mock, unittest, os

class InterfaceTest(unittest.TestCase):
    """Tests the launcher"""

    def setUp(self):
        interface = Interface()

    def tearDown(self):
        os.system('stty sane')

    def test_start(self):
        interface.content_manager.load = mock.Mock()
        interface.display.start = mock.Mock()

        interface.__start__()

        assert interface.content_manager.load.called, \
            "ContentManager failed to load"
        assert interface.display.start.called, \
            "Display failed to start"
