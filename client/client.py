#/bin/python
# This is a simple TCP client script
# used to test an echo server running on port 8880

import socket
import sys
from threading import Thread


class Client:

    def __init__(self, port=8888, host=socket.gethostname()):
        self.sock = socket.socket()

        self.sock.connect((host, port))

        name = raw_input("Please enter your nickname: ")
        self.sock.send('!name: '+name)

        thread1 = Thread(target=self.loop_output)
        thread2 = Thread(target=self.loop_input)
        thread1.start()
        thread2.start()

    def loop_input(self):
        while True:
            message = raw_input()
            self.sock.send(message)
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    def loop_output(self):
        while True:
            data = self.sock.recv(1024)

            if not data:
                break
            print data
        self.sock.close()
        sys.exit()

if __name__ == '__main__':
    client = Client()