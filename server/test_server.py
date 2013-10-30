import unittest
import socket
from server import Server


class Tests(unittest.TestCase):

    def create_server(self):
        port = 889
        host = 'localhost'

        # Creates a new instant of the Server class, it will also inherit
        # the Thread class.
        server = Server(port)

        # Start the new thread.
        server.start()

        # Creates a new socket with default parameters.
        self.sock = socket.socket()

        # Connects to the opened server on the specified port.
        self.sock.connect((host, port))

        # Send the server a command setting the name to 'test'.
        self.sock.send('!name: test')

        # Returns the server object.
        return server

    def test_one(self):

        # Creates the server. Just a form of code abstraction.
        server = self.create_server()

        # Listens for the welcome message from the server.
        data = self.sock.recv(1024)

        # Closes the client socket.
        self.sock.close()

        # Validates the received message.
        # If the message is a Welcome followed by a new line it pass.
        self.assertEqual(data, 'Welcome!\n')

        # Send a command to the server so it closes.
        server.__close__(self)

    def test_two(self):
        server = self.create_server()

        # Listens for the welcome message from the server.
        data = self.sock.recv(1024)

        # Listens for the status of a new client joining the room.
        data = self.sock.recv(1024)

        # Sends the server a command to return a list of present members.
        # As the server was created above it should only have one member.
        self.sock.send('!members')

        # Receives a list of members on the room.
        data = self.sock.recv(1024)
        self.sock.close()

        # If it returns just the name test it pass.
        self.assertEqual(data, 'test')
        server.__close__()


if __name__ == '__main__':
    unittest.main()
