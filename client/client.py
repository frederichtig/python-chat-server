#/bin/python
# This is a simple chat client used to test the chat server.
# You can open as many instances of it as you want.

import socket
from threading import Thread


class Client:

    def __init__(self, host=socket.gethostname(), port=888):
        """(str, int)

        Sets default values for port in which the socket will connect
        to 888, and the host to the current running the script.
        It can be changed on the class instantiation.
        """

        self.host = host
        self.port = port

        # Creates the socket with default parameters.
        self.sock = socket.socket()

    def run(self):

        # Connect the socket to the defined port and host.
        self.sock.connect((self.host, self.port))

        # Listen for the standard input to the user's nickname.
        name = raw_input("Please enter your nickname: ")

        # Send the server a message with the command name which sets the name
        # for the socket.
        self.sock.send('!name: '+name)

        # Sets a dedicated thread to writing the output to the screen.
        thread1 = Thread(target=self.loop_output)

        # Sets a dedicated thread to listening to user input.
        thread2 = Thread(target=self.loop_input)

        # Starts output thread first, so that we can read the server response
        # to user connection.
        thread1.start()

        # Starts the input thread and execute the function.
        thread2.start()

    def loop_input(self):
        """
        It handles user input to the server.
        """

        # Loops the input so that the user can constantly type.
        while True:

            # Reads the user input to the console.
            message = raw_input()

            # Send the server the entered message without any filtering.
            self.sock.send(message)

        # Shutdown reading (RD) and writing (WR) side of the socket.
        self.sock.shutdown(socket.SHUT_RDWR)

        # Close the socket so it can't be used anymore.
        self.sock.close()

    def loop_output(self):
        """
        It handles user output to the screen.
        """

        # Loops forever until no data is received.
        while True:

            # Blocking method that listen for incoming data, it listens
            # for at most 1024 bytes at once.
            data = self.sock.recv(1024)

            # If no data is received.
            if not data:

                # Exits the loop.
                break

            # Print the received data to the screen.
            print data

        # Shutdown reading (RD) and writing (WR) side of the socket.
        self.sock.shutdown(socket.SHUT_RDWR)

        # Close the socket so it can't be used anymore.
        self.sock.close()

# If running the script by itself the block gets executed.
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Instantiates the server class.
    client = Client()

    # Run the client.
    client.run()
