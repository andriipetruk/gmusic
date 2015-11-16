from objects.RequestHandler import RequestHandler
from objects.Controller import Controller
import mock, unittest, os

class RequestHandlerTest(unittest.TestCase):
    """Tests the launcher"""

    def test_parse(self):
        req = RequestHandler(None)
        req.send_to_controller = mock.Mock()

        req.parse('Test Data')

        self.assertTrue(req.send_to_controller.called, \
            "Send to controller was not called")
        req.send_to_controller.assert_called_once_with(['Test', 'Data'])

    def test_parse_single(self):
        req = RequestHandler(None)
        req.send_to_controller = mock.Mock()

        req.parse('Test')

        self.assertTrue(req.send_to_controller.called, \
            "Send to controller was not called")
        req.send_to_controller.assert_called_once_with(['Test', ''])


    def test_send_to_controller(self):
        controller = Controller(None)
        req = RequestHandler(controller)
        req.controller.typed_method = mock.Mock()

        req.send_to_controller(['method','data'])

        self.assertTrue(hasattr(req.controller, 'typed_method')), \
            "typed_method does not exist in Controller"
        self.assertTrue(req.controller.typed_method.called)
