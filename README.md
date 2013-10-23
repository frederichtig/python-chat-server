Python chat server
=================

This is a simple python chat server.
It is composed by a server and a client written
in Python 2.7 and a client written in HTML5 using
WebSockets.
It allows multiple clients at the same time, and
emits notifications every time a user enters/exits.
Users can use the following commands:
* `!members` show the online users.
* `!name: <name>` will update your name as long it
isn't been used by another person.
* `!quit` leaves the room.

### How to run

To run the server you can do it in two ways:

* Import the file into a terminal by entering
`from server import Server`, then you create a
new instance for that object by entering
`server = Server()`, and finally you can start
the server calling the run method, `server.run()`

* Run it as an executable, it will
automatically start.

If you run it by the first option you can
specify which port to use.

`Ex.: 'server = Server(888)'`

Make sure you use an available port, otherwise
the server will not run.

By the second option it creates the server
with the default port 888.

These steps also work for the client
script, just change 'Server/server' with
'Client/client'. However you can specify a
second argument on the object creation that
will refer to the host address, if you leave
it blank it will presume the server is running
on the same address.

### HTML5 Version

To accept WebSocket requests you need to run a
bridge between the client and the server, as a
WebSocket and TCP are different protocols.

I recommend using the Kaazing WebSocket Gateway.

* Go to [Kaazing developer downloads](http://developer.kaazing.com/downloads/).
* Choose the Custom Edition, download and install it.
* On the installation path find the 'gateway-config-minimal.xml' file.
* Add the following lines to it:
```
<service>
    <accept>ws://localhost:888/echo</accept>
    <connect>tcp://localhost:880</connect>
    <type>proxy</type>
    <cross-site-constraint>
        <allow-origin>*</allow-origin>
    </cross-site-constraint>
</service>
```

* `<accept>ws://localhost:8888/echo</accept>` is the address it receives incoming connections.
* `<connect>tcp://localhost:8880</connect>` is the address it will redirect those connections.

Make sure you run the server before the client.
