import logging
import logging.config

import hashlib
import socket
import json
import os

class Client:
    def __init__(self, ip, port, files, chunk, sock):
        self.ip = ip
        self.port = port
        self.files = files
        self.chunk = chunk
        self.sock = sock
    
    def connect(self):
        try:
            self.sock.connect((self.ip , self.port))
            logging.info('Log @connected to {}:{}'.format(self.ip, str(self.port)))
        except Exception as e:
            logging.error('Log @connect exception {}'.format(str(e)))

    def send(self):
        try:
            for i in self.files:
                f = open(i, 'rb')
                buf = f.read(self.chunk)
                while buf:
                    self.sock.send(buf)
                    buf = f.read(self.chunk)
                logging.info('Log @successfully sent: {}'.format(i))
                f.close()

        except Exception as e:
            logging.error('Log @send exception {}'.format(str(e)))

    def integrityCheck(self):
        md5sum = {i:hashlib.md5(open(i, 'rb').read()).hexdigest() for i in self.files}
        print(md5sum)

    def close(self):
        try:
            #self.sock.shutdown(SHUT_RDWR)
            self.sock.close()
            logging.info('Log @closing {}:{} connection'.format(self.ip, str(self.port)))
        except Exception as e:
            logging.error('Log @closing exception {}'.format(str(e)))

def initialize():
    #list all files in complete dir and add them into a list
    #first thing, load config.json to see the complete dir
    with open('config.json', 'r+') as conf:
        data = json.load(conf)
        if data['ready'] is False:
            print("[!] You must run setup.py first!")
            exit()
        else:
            complete = data['complete']
            ip = data['ip']
            port = data['port']
    if [f for f in os.listdir(complete) if not f.startswith('.')] == []:
        logging.info('Log @empty directory, exiting...')
    else:
        files = [complete+str(f) for f in os.listdir(complete)]
    chunk = 1024*8 #chunk of data
    sock = socket.socket() #socket
    logging.config.fileConfig("log_config.ini", disable_existing_loggers=False) #logiger

    #send files
    client = Client(ip, port, files, chunk, sock)
    client.connect()
    client.send()
    client.integrityCheck()
    client.close()

if __name__ == "__main__":
    initialize()
