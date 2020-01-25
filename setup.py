"""Initialize config.json"""
import json
import sys
import os
import subprocess

def packages(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def setupjson(confile):
    with open(confile, 'r+') as conf:
        data = json.load(conf)

        data['complete'] = input("[*] complete torrents dir: ")
        data['ip'] = input("[*] server's ip: ")
        data['port'] = int(input("[*] server's port: "))
        data['ready'] = True

        if os.path.exists(data["complete"]):
            conf.seek(0)
            conf.write(json.dumps(data, indent=4))
            conf.truncate()
        else:
            print("Invalid paths")

if __name__ == "__main__":
    owo = input("Would you like to receive desktop notifications on file transfers? (windows only) (y\\n) ")
    if owo == 'y':
        packages("win10toast")
    confile = "config.json"
    with open(confile, 'r+') as conf:
        data = json.load(conf)
        if data['ready'] is False:
            setupjson(confile)
        else:
            message = confile+" is already initialized, do you want to re-initialize it? (y\\n)"
            choice = input(message)
            if choice.lower() == 'y':
                setupjson(confile)
            else:
                exit()
