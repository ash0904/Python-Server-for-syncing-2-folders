import socket,os,time,sys,subprocess
import datetime
import hashlib

def get_mtime(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
sock = socket.socket()
host = "127.0.0.1"
port = 60000

sock.connect((host, port))

def Main():
    # print 'Server listening....'
    # client, addr = sock.accept() # addr = (ip,port) , waiting for connection
    l = raw_input("prompt> ")
    while (l != "quit"):
        sock.send(l) # send client message l
        args = l.split()
        if args[0] == "download":
            data = "ktb"
            fh = open(args[2], 'a+')
            while True:
                data = sock.recv(1024)
                if data == "zqqxq":
                    break
                fh.write(data)
            fh.close()
            # print "checking MD5sum"
            # print "Download complete!"
            print "File "+args[2]
        else:
            data = sock.recv(1024)
            print data
        l = raw_input("prompt> ")

    print('Connection Closed, Bye!')
    sock.send('Over')
    sock.close()

if __name__ == "__main__":
    Main()
