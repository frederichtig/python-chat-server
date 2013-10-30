#!/bin/python
# This is a chat server.
# A chat server will accept multiple connections at the same time, once a
# message is receive, it will send back to all other clients connected to
# the server. It also handles users disconnection and chat commands.

import socket
from threading import Thread


class Server(Thread):
    """
    This class inherits from the Thread object, so you can instantiate it
    and run it normally, calling run(), or you can run it as a new thread,
    calling start().
    """

    def __init__(self, port=888, host='0.0.0.0'):
        """(str, int)
        Set default values to 0.0.0.0, and port to
        888, it can be changed on the class
        instantiation.
        """

        # Initiates the Thread class when the Server class is instantiated.
        super(Server, self).__init__()

        # Variable used by loops to check if it should continue (server is
        # running).
        self.running = True

        # The first argument is the address family (IPv4), the second is
        # the socket type.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Sets an option to the socket to don't enter in a time wait
        # state and make the address available right away.
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Binds the port and host to the created socket.
        self.sock.bind((host, port))

        # Initializes the client list dictionary to handle individuals.
        self.clients = {}

    def run(self):

        # Blocking method that checks for connections on the socket.
        self.sock.listen(1)

        print "Server ready to receive connection"

        # Loops forever so that when the block is executed the program doesn't end.
        while self.running:

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
            print 'New connection by address {} on port {}'.format(address[0], address[1])

            # Start a new thread for each client so that each one can have its own
            # handling. The first arg is the user socket, the second its address.
            thread = Thread(target=self.client_handler, args=(user, address))

            # Start the thread and executes the client handling.
            thread.start()

    def client_handler(self, user, a):
        """(Socket)

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
                data = user.recv(1024)
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
                        if 'name' == data[data.index("!")+1:5]:

                            # Sets the variable name to anything after the colon.
                            name = data[data.index(":")+2:]

                            # Send a message to all users that the user with the
                            # name set above entered the chat.
                            self.sendall('', name + ' just got in.')

                            # Updates the client list with the set name.
                            self.clients[user] = name

                        # Otherwise checks if it contains 'members'.
                        elif 'members' == data[data.index("!")+1:8]:

                            # Creates a list with every client name in the clients
                            # list, leaving out the socket objects.
                            members = [self.clients[c] for c in self.clients]

                            # Send the user the list of connected members.
                            user.send(', '.join(members))

                        # Otherwise if the string contains quit.
                        elif 'quit' == data[data.index("!")+1:5]:

                            # Exit the loop so that closing can occur.
                            break

                        else:
                            # Sends the user a warning that the command is
                            # not found.
                            user.send('Unavailable command')

                    # If data is not a command.
                    else:

                        # Sends all the users the received message and the sender.
                        self.sendall(self.clients[user], " says: " + data)

                # If there's no data or it returns false we know that the client
                # is not connected anymore.
                else:

                    # Ends the loop.
                    break

        # Closes the client socket.
        user.close()

        # Sets a reference so that we can pass it to a function when it gets
        # deleted.
        username = self.clients[user]

        # Delete the client entry from the client list.
        del self.clients[user]

        # Emits a warning to all members that the user has left.
        self.sendall('', username + ' just left.')

    def sendall(self, s, message):
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

        # Sets the running condition to false so that a loop knows
        # that the server is closed.
        self.running = False

        # Closes the socket.
        self.sock.close()

# If running the script by itself the block gets executed.
if '__main__' == __name__:
    import doctest
    doctest.testmod()

    # Instantiates the server class.
    server = Server()

    # Run the server.
    server.run()


