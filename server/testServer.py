import unittest
import socket
import threading
from random import randint
from server import Server


class Tests(unittest.TestCase):

    def test_one(self):
        port = randint(2000,6000)
        # Here I use random port number so that I don't have to change
        # everytime I test. Sometimes the socket takes too long to close.
        host = 'localhost'
        thread = threading.Thread(target=Server, args=(host, port)).start()
        # Initializes a new thread so we can emulate the client side below.
        self.sock = socket.socket()
        self.sock.connect((host, port))
        # Connects to the newly created socket.
        self.sock.send('!name: test')
        # Send the server the name of test.
        data = self.sock.recv(1024)
        # Listens for the welcome message from the server.
        self.assertEqual(data, 'Welcome!\n')
        # If the message is a Welcome followed by a new line it pass.

    def test_two(self):
        port = randint(2000,6000)
        # Again I use random port number so that it doesn't conflict to the
        # previous opened socket.
        host = 'localhost'
        thread = threading.Thread(target=Server, args=(host, port)).start()
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.sock.send('!name: test')
        data = self.sock.recv(1024)
        # Listens for the welcome message from the server.
        data = self.sock.recv(1024)
        # Listens for the status of a new client joining the room.
        self.sock.send('!members')
        # Sends the server a command to return a list of present members.
        # As the server was created above it only has one member. The test user.
        data = self.sock.recv(1024)
        # Receives a list of members on the room.
        self.assertEqual(data, 'test')
        # If it returns just the name test it pass.


if __name__ == '__main__':
    unittest.main()
