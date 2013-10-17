#!/bin/python

import socket
from threading import Thread


class Server:

    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(3)

        self.clients = {}

        print "Server ready to receive connection"

        while True:
            user, address = sock.accept()
            self.clients[user] = ""
            user.send('Welcome!\n')
            print 'New connection by ', user
            thread = Thread(target=self.client_handler, args=(user, address))
            thread.start()

        sock.close()

    def client_handler(self, s, a):
        while True:
            try:
                data = s.recv(1024)
                print data
            except:
                break
            else:
                if data:
                    if data.startswith("!"):
                        if data[data.index("!")+1:5] == 'name':
                            name = data[data.index(":")+2:]
                            self.msg_send('', name + ' just got in.')
                            self.clients[s] = name
                        elif data[data.index("!")+1:8] == 'members':
                            members = [self.clients[c] for c in self.clients]
                            s.send(', '.join(members))
                        elif 'quit' == data[data.index("!")+1:5]:
                            break
                        else:
                            s.send('Unavailable command')
                    else:
                        self.msg_send(self.clients[s], " says: " + data)
                else:
                    break

        s.close()
        username = self.clients[s]
        del self.clients[s]
        self.msg_send('', username + ' just left.')

    def msg_send(self, s, message):
        print message
        for user in self.clients:
            user.send(s + message)

if __name__ == '__main__':
    server = Server("0.0.0.0", 8888)