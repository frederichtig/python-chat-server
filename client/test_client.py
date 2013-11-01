import os
import sys
import unittest
from time import sleep
from client import Client

foo_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
sys.path.append(os.path.normpath(os.path.join(foo_dir, '..', '..')))
from Server.server import Server


class IoObj():
    def __init__(self, arr):
        self.output = self.input = ''
        self.l = 0
        self.a = arr
        self.locked = True

    def read(self, void=None):
        while self.locked:
            sleep(0.1)

        self.locked = True
        return self.input

    def write(self, message):
        self.output = message

    def get_messages(self):
        self.locked = False

    def send_message(self, message):
        self.input = message
        self.locked = False


class Tests(unittest.TestCase):

    port = 890
    host = 'localhost'

    def start_server(self):
        server = Server(self.port)
        server.start()
        return server

    def create_client(self, input, output=sys.stdout):
        client = Client(self.port, name=input, output=output)
        client.start()
        return client

    def test_one(self):
        io_obj = IoObj(['name', 'Hello Buddy'])
        server = self.start_server()
        sender = self.create_client(io_obj.read, io_obj.write)
        sleep(0.1)
        io_obj.send_message('name')
        sleep(0.1)
        io_obj.send_message('Hello Buddy')
        sleep(0.1)
        io_obj.get_messages()

        self.assertEqual("name says: Hello Buddy\n", io_obj.output)

        io_obj.locked = False
        sender.__close__()
        server.__close__()

if '__main__' == __name__:
    unittest.main()