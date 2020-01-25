import socket
import pickle
import json

#from win10toast import ToastNotifier

class Server:
    def __init__(self, port, sock, chunk, filenames, toaster):
        self.sock = sock
        self.chunk = chunk
        self.toaster = toaster
        self.port = port
        self.filenames = filenames
    
    def bindsock(self):
        self.sock.bind(('127.0.0.1', self.port))
        self.sock.listen(5)

    def initfiles(self):
        while True:
            client, addr = self.sock.accept()
            buf = client.recv(self.chunk)
            if buf:
                self.filenames = pickle.loads(buf)
            client.close()
            break

    def receive(self):
        while True:
            client, addr = self.sock.accept()
            buf = client.recv(self.chunk)

def initialize():
    with open('config.json', 'r+') as conf:
        data = json.load(conf)
        port = data['port']
    
    sock = socket.socket()
    chunk = 1024*8
    #toaster = ToastNotifier()
    toaster = 0
    filenames = []

    server = Server(port, sock, chunk, filenames, toaster)
    server.bindsock()
    server.initfiles()
    server.receive()

if __name__ == "__main__":
    with open('config.json', 'r+') as conf:
        data = json.load(conf)
        if data['ready'] is False:
            print("[!] You must run setup.py first!")
            exit()
    initialize()
