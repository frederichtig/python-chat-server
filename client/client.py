#/bin/python
# This is a simple chat client used to test the chat server.
# You can open as many instances of it as you want.

import sys
import socket
from threading import Thread


class Client(Thread):

    def __init__(self, port=888, host=socket.gethostname(), name=raw_input, output=sys.stdout.write):
        """
        Sets default values for port in which the socket will connect
        to 888, and the host to the current running the script.
        It can be changed on the class instantiation.

        @type port: int
        @type host: str
        """

        # Initiates the Thread class when the Server class is instantiated.
        super(Client, self).__init__()

        self.input = name
        self.output = output

        # Variable used by loops to check if it should continue (client is
        # connected).
        self.running = True

        self.host = host
        self.port = port

        # Creates the socket with default parameters.
        self.sock = socket.socket()

    def run(self):

        # Connect the socket to the defined port and host.
        self.sock.connect((self.host, self.port))

        # Checks if the user name isn't defined yet.

        # Listen for the standard input to the user's nickname.
        name = self.input("Please enter your nickname: ")

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
        while self.running:

            # Reads the user input to the console.
            message = self.input()

            # Send the server the entered message without any filtering.
            self.sock.send(message)

    def loop_output(self):
        """
        It handles user output to the screen.
        """

        # Loops forever until no data is received.
        while self.running:

            # Blocking method that listen for incoming data, it listens
            # for at most 1024 bytes at once.
            data = self.sock.recv(1024)

            # If no data is received.
            if not data:

                # Exits the loop.
                break

            # Print the received data to the screen.
            self.output(data+'\n')

    def __close__(self):
        # Sets the running condition to false so that a loop knows
        # that the client is disconnected.
        self.running = False

        # Close the socket so it can't be used anymore.
        self.sock.close()

# If running the script by itself the block gets executed.
if '__main__' == __name__:
    import doctest
    doctest.testmod()

    # Instantiates the server class.
    client = Client()

    # Run the client.
    client.run()