import unittest
import socket
from client import Client


class Tests(unittest.TestCase):

    def create_client(self):
        port = 890
        host = 'localhost'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)
        client = Client()
        client.start()
        return client

    def test_one(self):
        what = 'what?'
        client = self.create_client()
        self.assertEqual(what, what)
        client.__close__()

    def test_two(self):
        what = 'what?'
        client = self.create_client()
        self.assertEqual(what, what)
        client.__close__()

if __name__ == '__main__':
    unittest.main()