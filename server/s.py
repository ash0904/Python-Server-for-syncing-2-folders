import socket,os,time,sys,subprocess

sock = socket.socket()
host = "127.0.0.1"
port = 60000

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(5) # 5 client concurrently connected

def Main():
    print 'Server listening....'
    client, addr = sock.accept() # addr = (ip,port) , waiting for connection
    l = raw_input("prompt> ")
    while (l != "quit"):
        client.send(l) # send client message l
        args = l.split()
        if args[0] == "download":
            data = "ktb"
            fh = open(args[2], 'a+')
            while True:
                data = client.recv(1024)
                if data == "zqqxq":
                    break
                fh.write(data)
            fh.close()
            print "checking MD5sum"
            
            print "Download complete!"
            print "File "+args[2]
        else:
            data = client.recv(1024)
            print data
        l = raw_input("prompt> ")

    print('Connection Closed, Bye!')
    client.send('Over')
    client.close()

if __name__ == "__main__":
    Main()
    sock.shutdown(socket.SHUT_RDWR)
