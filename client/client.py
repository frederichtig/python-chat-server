#/bin/python
# This is a simple chat client used to test the chat server.
# You can open as many instances of it as you want.

import socket
from threading import Thread


class Client:

    def __init__(self, port=888, host=socket.gethostname()):
        """(int, string)

        Sets default values for port in which the socket will connect
        to 888, and the host to the current running the script.
        It can be changed on the class instantiation.
        """

        self.sock = socket.socket()
        # Creates the socket with default parameters.
        self.sock.connect((host, port))
        # Connect the socket to the defined port and host.
        name = raw_input("Please enter your nickname: ")
        # Listen for the standard input to the user's nickname.
        self.sock.send('!name: '+name)
        # Send the server a message with the command name which sets the name
        # for the socket.

        thread1 = Thread(target=self.loop_output)
        # Sets a dedicated thread to writing the output to the screen.
        thread2 = Thread(target=self.loop_input)
        # Sets a dedicated thread to listening to user input.
        thread1.start()
        # Starts output thread first, so that we can read the server response
        # to user connection.
        thread2.start()
        # Starts the input thread and execute the function.

    def loop_input(self):
        """
        This is a static method.
        It handles user input to the server.
        """
        while True:
        # Loops the input so that the user can constantly type.
            message = raw_input()
            # Reads the user input to the console.
            self.sock.send(message)
            # Send the server the entered message without any filtering.
        self.sock.shutdown(socket.SHUT_RDWR)
        # Shutdown reading (RD) and writing (WR) side of the socket.
        self.sock.close()
        # Close the socket so it can't be used anymore.

    def loop_output(self):
        """
        This is a static method.
        It handles user output to the screen.
        """
        while True:
        # Loops forever until no data is received.
            data = self.sock.recv(1024)
            # Blocking method that listen for incoming data, it listens
            # for at most 1024 bytes at once.

            if not data:
            # If no data is received.
                break
                # Exits the loop.
            print data
            # Print the received data to the screen.
        self.sock.shutdown(socket.SHUT_RDWR)
        # Shutdown reading (RD) and writing (WR) side of the socket.
        self.sock.close()
        # Close the socket so it can't be used anymore.

if __name__ == '__main__':
# If running the script by itself the block gets executed.
    import doctest
    doctest.testmod()
    client = Client()
    # Instantiates and initialize the server class.