from flask_socketio import SocketIOTestClient
import unittest
from app import app, socketio

class TestSocketIO(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = SocketIOTestClient(app, socketio)

    def test_word_broadcast(self):
        self.client.emit('send_word', {'word': 'hello'})
        received = self.client.get_received()
        self.assertTrue(any(msg['name'] == 'display_word' for msg in received))
        self.assertTrue(any('hello' in msg['args'][0]['word'] for msg in received))

    def tearDown(self):
        self.client.disconnect()

if __name__ == '__main__':
    unittest.main()
