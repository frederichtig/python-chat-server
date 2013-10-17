import unittest
import socket
import threading
from server import Server


class Tests(unittest.TestCase):

    def test_one(self):
        port = 1234
        host = 'localhost'
        thread = threading.Thread(target=Server, args=(host, port)).start()
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.sock.send('!name: test')
        data = self.sock.recv(1024)
        self.assertEqual(data, 'Welcome!\n')
        #print threading.Event().set()
        #print thread.terminate()


if __name__ == '__main__':
    unittest.main()
