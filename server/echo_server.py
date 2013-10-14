#!/bin/python

import socket
import threading


class Server:

    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(3)

        print "Server ready to receive connection"

        sockets = []
        clients = {}

        def client_handler(s, a):
            while True:
                data = s.recv(1024)

                if data:
                    if data.startswith("!"):
                        if data[data.index("!")+1:5] == 'name':
                            name = data[data.index(":")+2:]
                            clients[s] = name
                            print clients[s]
                        elif data[data.index("!")+1:8] == 'members':
                            s.send(', '.join([clients[c] for c in clients]))
                        elif 'quit' == data[data.index("!")+1:5]:
                            s.close()
                        else:
                            s.send('Unavailable command')
                    else:
                        for user in sockets:
                            if user != s:
                                user.send('' + clients[s].capitalize() + " says: " + data)
                        print "Received ", data

        while True:
            client, address = server_socket.accept()
            sockets.append(client)
            clients[client] = ""
            client.send('Welcome!\n')
            print 'New connection by ', client
            thread = threading.Thread(target=client_handler, args=(client, address))
            thread.start()

        server_socket.close()

server = Server("0.0.0.0", 8888)
server.run()

