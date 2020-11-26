from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

import warnings
warnings.filterwarnings('ignore')

class Server():
    def __init__(self):
        """Constructor function for building the server section of the Chat Server"""
       #Clients and Addresses
        self.clients = {}
        self.addresses = {}

        #Constants
        self.HOST = "127.0.0.1"
        self.PORT = 5000
        self.BUFFER_SIZE = 1024
        self.ADDR = (self.HOST, self.PORT)
        self.SOCK = socket(AF_INET, SOCK_STREAM)
        self.SOCK.bind(self.ADDR)
       
       #Thread
        self.accept_thread = None

    def accept_clients(self):
        """Function for handling for incoming clients."""
        while True:
            client, client_address = self.SOCK.accept()
            print("%s:%s has connected." % client_address)
            client.send("Welcome to the Messaging Platform. ".encode("utf8"))
            client.send("Enter your name and continue".encode("utf8"))
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client, client_address)).start()

    def handle_client(self, connection, address):  
        """Function for handling a single client connection."""
        name = connection.recv(self.BUFFER_SIZE).decode("utf8")
        welcome_message = 'Hi there, %s! If you ever want to leave the chat, type QUIT or press the Quit button.' % name
        connection.send(bytes(welcome_message, "utf8"))
        message = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(address[0], address[1]))
        self.broadcast_message(bytes(message, "utf8"))
        self.clients[connection] = name
        while True:
            message = connection.recv(self.BUFFER_SIZE)
            if message != bytes("QUIT", "utf8"):
                self.broadcast_message(message, name + ": ")
            else:
                connection.send(bytes("QUIT", "utf8"))
                connection.close()
                del self.clients[connection]
                self.broadcast_message(bytes("%s has left the chat." % name, "utf8"))
                break


    def broadcast_message(self, message, prefix=""):  
        """Function for broadcasting a message to all the clients."""
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + message)

    
    def server_functionality(self):
        """Function for establishing the server"""
        self.SOCK.listen(5)  
        print("Messaging Platform is active now")
        print("Waiting for people to join the platform...")
        self.accept_thread = Thread(target=self.accept_clients)
        self.accept_thread.start()  
        self.accept_thread.join()
        self.SOCK.close()

server= Server()
server.server_functionality()
