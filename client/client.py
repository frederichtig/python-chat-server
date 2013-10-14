#/bin/python
# This is a simple TCP client script
# used to test an echo server running on port 8880

import socket
from threading import Thread

# Create the socket object
client_socket = socket.socket()

# Assume the server is running on the same host as this client
host = socket.gethostname()

# Assume the server is running on port 8880
port = 8880

# Connect to the server
client_socket.connect((host, port))

# This is the list of messages this client will send to the echo server
name = raw_input("Please enter your nickname: ")
client_socket.send('!name: '+name)


def loop_input():
    while True:
        message = raw_input()
        client_socket.send(message)


def loop_output():
    while True:
        data = client_socket.recv(1024)
        print data

thread1 = Thread(target=loop_output)
thread2 = Thread(target=loop_input)
thread1.start()
thread2.start()
while True:
    loop_output()
    loop_input()
        # Always remember to close the socket
client_socket.close()
