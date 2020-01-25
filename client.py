import logging
import logging.config

import hashlib
import pickle
import socket
import time
import json
import os

from functools import partial

transferredHash = None

class Client:
    def __init__(self, ip, port, files, filenames, chunk, sock):
        self.ip = ip
        self.port = port
        self.files = files
        self.filenames = filenames
        self.chunk = chunk
        self.sock = sock
    
    def sockConnect(self):
        try:
            self.sock.connect((self.ip , self.port))
            logging.info('Log @connected to {}:{}'.format(self.ip, str(self.port)))
        except Exception as e:
            logging.error('Log @connect exception {}'.format(str(e)))

    def sockSend(self):
        try:
            global transferredHash
            #send filenames
            data = pickle.dumps(self.filenames[0])
            self.sock.send(data)
            
            f = open(self.files[0], 'rb')
            buf = f.read(self.chunk)
            while buf:
                self.sock.send(buf)
                buf = f.read(self.chunk)
            f.close()
            self.sock.shutdown(socket.SHUT_WR)
            
            #check integrity
            transferredHash = self.sock.recv(1024).decode()
            print(transferredHash)

            logging.info('Log @successfully sent: {}'.format(self.filenames[0])) 
        except Exception as e:
            logging.error('Log @send exception {}'.format(str(e)))

    def sockClose(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            logging.info('Log @closing {}:{} connection'.format(self.ip, str(self.port)))
        except Exception as e:
            logging.error('Log @closing exception {}'.format(str(e)))

def deleteFile(files):
        os.remove(files)

def md5(fname):
        with open(fname, 'rb') as f:
            d = hashlib.md5()
            for buf in iter(partial(f.read, 128), b''):
                d.update(buf)
        return d.hexdigest()

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
        filenames = [str(f) for f in sorted(os.listdir(complete))]
        files = [complete+str(f) for f in sorted(os.listdir(complete))]
    chunk = 1024*8 #chunk of data
    sock = socket.socket() #socket
    logging.config.fileConfig("log_config.ini", disable_existing_loggers=False) #logiger

    try:
        client = Client(ip, port, files, filenames, chunk, sock)
        client.sockConnect()
        client.sockSend()
        client.sockClose()
    except UnboundLocalError as unbound:
        logging.warning('Log @warning torrents dir is empty!')
        exit()
    except Exception as e:
        logging.error('Log @error {}'.format(str(e)))
        exit()

    if md5(files[0]) == transferredHash:
        deleteFile(files[0])
        logging.info('Log @info removed file from torrentbox, have fun')
    else:
        logging.warning('Log @warning md5 does not match, retrying...')
        exit()

if __name__ == "__main__":
    initialize()
