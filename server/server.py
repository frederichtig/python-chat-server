#!/bin/python
# This is a chat server.
# A chat server will accept multiple connections at the same time, once a
# message is receive, it will send back to all other clients connected to
# the server. It also handles users disconnection and chat commands.

import socket
#from threading import Thread
import threading


class Server:

    def __init__(self, host='0.0.0.0', port=888):
        """(str, int)
        Set default values to 0.0.0.0, and port to
        888, it can be changed on the class
        instantiation.
        """

        self.host = host
        self.port = port
        self.RUNNING = True

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # The first argument is the address family (IPv4), the second is
        # the socket type.
        sock.bind((self.host, self.port))
        # Binds the port and host to the created socket.
        sock.listen(1)
        # Blocking method that checks for connections on the socket.
        self.clients = {}
        # Initializes the client list dictionary to handle individuals.
        self.threads = []

        print "Server ready to receive connection"

        while self.RUNNING:
        # Loops forever so that when the block is executed the program doesn't end.

            user, address = sock.accept()
            # Blocking method that accepts connection on the socket listening.
            # The first argument is the client socket, the second is the address
            # bound for that client.
            self.clients[user] = ''
            # Creates the entry for the user in the client list but do not set a
            # name for the socket yet, because message handler is on another
            # block.
            user.send('Welcome!\n')
            # Greets the user.
            print 'New connection by ', user
            # Print the socket to the server just for control purposes.
            thread = threading.Thread(target=self.client_handler, args=(user, address))
            # Start a new thread for each client so that each one can have its own
            # handling. The first arg is the user socket, the second its address.
            thread.start()
            # Start the thread and executes the client handling.

        sock.close()
        # If the loop breaks the socket is closed.

    def client_handler(self, s, a):
        """(Socket, tuple)

        This method will handle clients incoming messages and pass them to all
        other connected members. It also checks if received data is a command
        and executes the appropriate action for its caller.
        """
        while self.RUNNING:
        # Loops forever so that the we always listen for data from the client.
            try:
            # Uses a try block so that when the data throws an exception it gets
            # handled, making the server not crash.
                data = s.recv(1024)
                # Blocking method that listen for incoming data, it listens
                # for at most 1024 bytes at once.
                print data
            except:
            # Usually data throws an exception when the user forcefully
            # disconnects or when the user exits the terminal (KeyboardInterrupt).
                break
                # Ends the loop.
            else:
            # If not exception is thrown.
                if data:
                # Checks if there's any data.
                    if data.startswith("!"):
                    # Checks if the data starts with a '!' (Command sign).
                        if data[data.index("!")+1:5] == 'name':
                        # Checks if the the string contains 'name' after the '!'.
                            name = data[data.index(":")+2:]
                            # Sets the variable name to anything after the colon.
                            self.msg_send('', name + ' just got in.')
                            # Send a message to all users that the user with the
                            # name set above entered the chat.
                            self.clients[s] = name
                            # Updates the client list with the set name.
                        elif data[data.index("!")+1:8] == 'members':
                        # Otherwise checks if it contains 'members'.
                            members = [self.clients[c] for c in self.clients]
                            # Creates a list with every client name in the clients
                            # list, leaving out the socket objects.
                            s.send(', '.join(members))
                            # Send the user the list of connected members.
                        elif 'quit' == data[data.index("!")+1:5]:
                        # Otherwise if the string contains quit.
                            break
                            # Exit the loop so that closing can occur.
                        else:
                            s.send('Unavailable command')
                            # Sends the user a warning that the command is
                            # not found.
                    else:
                    # If data is not a command.
                        self.msg_send(self.clients[s], " says: " + data)
                        # Sends all the users the received message and the sender.
                else:
                # If there's no data or it returns false we know that the client
                # is not connected anymore.
                    break
                    # Ends the loop.

        s.close()
        # Closes the client socket.
        username = self.clients[s]
        # Sets a reference so that we can pass it to a function when it gets
        # deleted.
        del self.clients[s]
        # Delete the client entry from the client list.
        self.msg_send('', username + ' just left.')
        # Emits a warning to all members that the user has left.

    def msg_send(self, s, message):
        """(Socket, string)

        This method iterates on all the clients on the client list, sending
        each one the sender (s) as prefix and the message (message).
        If it is a system message the (s) can be an empty string.
        """

        for user in self.clients:
        # Iterates on the client list
            user.send(s + message)
            # Uses the client's socket to send the message

    def __close__(self):
        self.RUNNING = False

if __name__ == '__main__':
# If running the script by itself the block gets executed.
    import doctest
    doctest.testmod()
    server = Server()
    # Instantiates and initialize the server class.
