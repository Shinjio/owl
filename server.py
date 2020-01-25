import hashlib
import socket
import pickle
import time
import json

from win10toast import ToastNotifier

class Server:
    def __init__(self, port, sock, chunk, toaster):
        self.sock = sock
        self.chunk = chunk
        self.toaster = toaster
        self.port = port
        self.filenames = None
    
    def bindsock(self):
        self.sock.bind(('127.0.0.1', self.port))
        self.sock.listen(5)

    def initfiles(self):
            client, addr = self.sock.accept()
            buf = client.recv(self.chunk)
            if buf:
                self.filenames = pickle.loads(buf)
            print(self.filenames)
            if self.filenames is not None:
                self.receive(client, addr)

    def receive(self, client, addr):
        f = open(self.filenames, 'wb')
        buf = client.recv(self.chunk)
        while buf:
            f.write(buf)
            buf = client.recv(self.chunk)
        f.close()
        result = self.md5(self.filenames)
        print(result)
        client.send(result.encode())
        self.success(self.filenames)
        self.initfiles()

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(1024), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def success(self, filename):
        toaster.show_toast("owl file transfer", "{} transferred successfully!",
                threaded=True, icon_path=None, duration = 5)
        while toaster.notification_active():
            time.sleep(0.1)

def initialize():
    with open('config.json', 'r+') as conf:
        data = json.load(conf)
        port = data['port']
    
    sock = socket.socket()
    chunk = 1024*8
    toaster = ToastNotifier()
    
    server = Server(port, sock, chunk, toaster)
    server.bindsock()
    server.initfiles()

if __name__ == "__main__":
    with open('config.json', 'r+') as conf:
        data = json.load(conf)
        if data['ready'] is False:
            print("[!] You must run setup.py first!")
            exit()
    initialize()
