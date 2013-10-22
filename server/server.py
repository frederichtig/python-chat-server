#!/bin/python
# This is a chat server.
# A chat server will accept multiple connections at the same time, once a
# message is receive, it will send back to all other clients connected to
# the server. It also handles users disconnection and chat commands.

import socket
from threading import Thread


class Server:

    def __init__(self, port=888, host='0.0.0.0'):
        """(str, int)
        Set default values to 0.0.0.0, and port to
        888, it can be changed on the class
        instantiation.
        """

        # The first argument is the address family (IPv4), the second is
        # the socket type.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binds the port and host to the created socket.
        self.sock.bind((host, port))

        # Initializes the client list dictionary to handle individuals.
        self.clients = {}

    def run(self):

        # Blocking method that checks for connections on the socket.
        self.sock.listen(1)

        print "Server ready to receive connection"

        # Loops forever so that when the block is executed the program doesn't end.
        while True:

            # Blocking method that accepts connection on the socket listening.
            # The first argument is the client socket, the second is the address
            # bound for that client.
            user, address = self.sock.accept()

            # Creates the entry for the user in the client list but do not set a
            # name for the socket yet, because message handler is on another
            # block.
            self.clients[user] = ''

            # Greets the user.
            user.send('Welcome!\n')

            # Print the socket to the server just for control purposes.
            print 'New connection by ', user

            # Start a new thread for each client so that each one can have its own
            # handling. The first arg is the user socket, the second its address.
            thread = Thread(target=self.client_handler, args=(user, address))

            # Start the thread and executes the client handling.
            thread.start()

        # If the loop breaks the socket is closed.
        self.sock.close()

    def client_handler(self, s, a):
        """(Socket, tuple)

        This method will handle clients incoming messages and pass them to all
        other connected members. It also checks if received data is a command
        and executes the appropriate action for its caller.
        """

        # Loops forever so that the we always listen for data from the client.
        while True:

            # Uses a try block so that when the data throws an exception it gets
            # handled, making the server not crash.
            try:

                # Blocking method that listen for incoming data, it listens
                # for at most 1024 bytes at once.
                data = s.recv(1024)
                print data

            # Usually data throws an exception when the user forcefully
            # disconnects or when the user exits the terminal (KeyboardInterrupt).
            except:

                # Ends the loop.
                break

            # If not exception is thrown.
            else:

                # Checks if there's any data.
                if data:

                    # Checks if the data starts with a '!' (Command sign).
                    if data.startswith("!"):

                        # Checks if the the string contains 'name' after the '!'.
                        if data[data.index("!")+1:5] == 'name':

                            # Sets the variable name to anything after the colon.
                            name = data[data.index(":")+2:]

                            # Send a message to all users that the user with the
                            # name set above entered the chat.
                            self.msg_send('', name + ' just got in.')

                            # Updates the client list with the set name.
                            self.clients[s] = name

                        # Otherwise checks if it contains 'members'.
                        elif data[data.index("!")+1:8] == 'members':

                            # Creates a list with every client name in the clients
                            # list, leaving out the socket objects.
                            members = [self.clients[c] for c in self.clients]

                            # Send the user the list of connected members.
                            s.send(', '.join(members))

                        # Otherwise if the string contains quit.
                        elif 'quit' == data[data.index("!")+1:5]:

                            # Exit the loop so that closing can occur.
                            break

                        else:
                            # Sends the user a warning that the command is
                            # not found.
                            s.send('Unavailable command')

                    # If data is not a command.
                    else:

                        # Sends all the users the received message and the sender.
                        self.msg_send(self.clients[s], " says: " + data)

                # If there's no data or it returns false we know that the client
                # is not connected anymore.
                else:

                    # Ends the loop.
                    break

        # Closes the client socket.
        s.close()

        # Sets a reference so that we can pass it to a function when it gets
        # deleted.
        username = self.clients[s]

        # Delete the client entry from the client list.
        del self.clients[s]

        # Emits a warning to all members that the user has left.
        self.msg_send('', username + ' just left.')

    def msg_send(self, s, message):
        """(Socket, string)

        This method iterates on all the clients on the client list, sending
        each one the sender (s) as prefix and the message (message).
        If it is a system message the (s) can be an empty string.
        """

        # Iterates on the client list.
        for user in self.clients:

            # Uses the client's socket to send the message.
            user.send(s + message)

    def __close__(self):
        self.sock.close()

# If running the script by itself the block gets executed.
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Instantiates the server class.
    server = Server()

    # Run the server.
    server.run()


