import socket,os,time,sys,subprocess
import datetime
import hashlib

#TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 60000
sock.connect((host, port))

#UDP socket
sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
portudp = 61000
sockudp.bind((host, portudp))

def Main():
    l = raw_input("prompt> ")
    tries=0
    while (l != "quit"):
        sock.send(l) # send server message l
        args = l.split()
        if args[0] == "download" and len(args) == 3:
            if os.path.isfile(args[2]):
                os.remove(args[2])
            if sock.recv(1024)  == "Exist":
                if args[1] == "TCP":
                    fh = open(args[2], 'a+')
                    while True:
                        data = sock.recv(1024)
                        if data == "zqqxq":
                            break
                        fh.write(data)
                    fh.close()
                    print "File Received: "+args[2]

                elif args[1] == "UDP":
                    fh = open(args[2], 'a+')
                    while True:
                        data, addre = sockudp.recvfrom(1024)
                        # print "data s= ", data
                        if data[:5] == "zqqxq":
                            break
                        fh.write(data)
                    fh.close()
                    md5 = hashlib.md5(open(args[2], 'rb').read()).hexdigest()
                    recv_md5 = data[5:]
                    print "md5 =     ",md5
                    print "recv_md5= ",recv_md5
                    if recv_md5 == md5:
                        print "File Receive succesfull"
                    else:
                        print "File Receive unsuccesfull"
                        l="".join(l)
                        tries += 1
                        # print "l= ", l
                        if tries <10:
                            continue
                        else:
                            tries=0
                            print "Unsuccesful after 10 tries"
            else:
                print "No such File Exist"
        else:
            data = sock.recv(1024)
            print data
        l = raw_input("prompt> ")

    print('Connection Closed, Bye!')
    sock.send('Close')
    sock.close()
    sockudp.close()

if __name__ == "__main__":
    Main()
