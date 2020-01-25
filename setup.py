"""Initialize config.json"""
import json
import os

def validate(path1, path2):
    return True if os.path.exists(path1) and os.path.exists(path2) else False

def setup(confile):
    with open(confile, 'r+') as conf:
        data = json.load(conf)

        data['complete'] = input("[*] complete torrents dir: ")
        data['incomplete'] = input("[*] incomplete torrents dir: ")
        data['ip'] = input("[*] server's ip: ")
        data['port'] = int(input("[*] server's port: "))
        data['ready'] = True

        if validate(data['complete'], data['incomplete']):
            conf.seek(0)
            conf.write(json.dumps(data, indent=4))
            conf.truncate()
        else:
            print("Invalid paths")

if __name__ == "__main__":
    confile = "config.json"
    with open(confile, 'r+') as conf:
        data = json.load(conf)
        if data['ready'] is False:
            setup(confile)
        else:
            message = confile+" is already initialized, do you want to re-initialize it? (y\\n)"
            choice = input(message)
            if choice.lower() == 'y':
                setup(confile)
            else:
                exit()
