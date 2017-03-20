import socket,os,time,sys,subprocess
import datetime
import hashlib

def get_mtime(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

sock = socket.socket()
host = "127.0.0.1"
port = 60000

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(5) # 5 client concurrently connected

def Main():
    print('server starts...')
    client, addr = sock.accept() # addr = (ip,port) , waiting for connection
    while True:
        data = client.recv(1024)
        print('request = %s' %(data))
        if data=="Over":
            break
        args = data.split()
        if not args:
            ls = "Please enter the command"
            client.send(ls)
        elif args[0]== "index":
            if len(args) == 1:
                ls = os.popen('ls').read()
            elif args[1] == "longlist" :
                    ls = os.popen('ls -l').read()
            elif args[1] == "shortlist" :
                ls = os.popen('ls').read()
                fs = ls.split()
                # fl =[]
                for it in range(len(fs)):
                    temp = get_mtime(fs[it])
                    fs[it] = fs[it] + " " +str(temp)
                ls = "\n".join(fs)
            else:
                ls = "please check the syntax"
            client.send(ls)
        elif args[0] == "hash":
            if len(args) < 2:
                ck = "please provide arguments"
            elif args[1] == "verify":
                if not args[2]:
                    ck = "Enter File name"
                else:
                    comm = "cksum " + args[2]
                    ck = os.popen(comm).read()
                # print ck
            else:
                ck = "please check the syntax"
            client.send(ck)
        elif args[0] == "download" and len(args)==3:
            if args[1] == "TCP":
                with open(args[2]) as fileobject:
                    for line in fileobject:
                        client.send(line)
                time.sleep(1)
                client.send("zqqxq")
            elif args[1] == "UDP":
                with open(args[2]) as fileobject:
                    for line in fileobject:
                        client.send(line)
                time.sleep(1)
                client.send("zqqxq")
            else:
                ls = "Enter TCP or UDP as second argument"
                client.send(ls)
        else:
            ls = "Please check command or Format"
            client.send(ls)
    client.close()
    print('connection closed, Bye!')


if __name__ == "__main__":
    Main()
    sock.shutdown(socket.SHUT_RDWR)
