import os
import sys
import unittest
from time import sleep
from client import Client

foo_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
sys.path.append(os.path.normpath(os.path.join(foo_dir, '..', '..')))
from Server.server import Server


class Tests(unittest.TestCase):

    port = 890
    host = 'localhost'
    test_message = "Hello world."

    class OutTest:
        def __init__(self):
            self.message = ''

        def write(self, message):
            print("I got the message: " + message)
            self.message = message

        def get_message(self):
            return self.message

    def start_server(self):
        server = Server(self.port)
        server.start()
        return server

    def create_client(self, out=sys.stdout):
        client = Client(port=self.port, input=self.myrawinput, out=out)
        client.start()
        return client

    def myrawinput(self, message):
        return "name"

    def test_one(self):
        server = self.start_server()
        sleep(0.5)
        out_mock = self.OutTest()
        sender = self.create_client()
        sleep(0.5)
        receiver = self.create_client(out_mock)
        sleep(0.5)

        sender.send_message("Hello Buddy")
        sleep(0.5)

        self.assertEqual("name says: Hello Buddy\n", out_mock.get_message())

        sender.__close__()
        receiver.__close__()
        server.__close__()

if '__main__' == __name__:
    unittest.main()