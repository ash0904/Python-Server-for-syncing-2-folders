import socket,os,time,commands,sys,subprocess
import datetime
import hashlib

#TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 60000
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(5) # 5 client concurrently connected

#UDP socket
sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostudp = "127.0.0.1"
portudp = 61000

def get_mtime(filename):
    t = time.ctime(os.path.getmtime(filename))
    # t = datetime.datetime.fromtimestamp(t)
    return t

def check_time(t1,st1,end1):
    t = datetime.datetime.strptime(t1, "%a %b %d %H:%M:%S %Y") #Thu Mar  9 00:54:18 2017
    st = datetime.datetime.strptime(st1, "%a %b %d %H:%M:%S %Y")
    end = datetime.datetime.strptime(end1, "%a %b %d %H:%M:%S %Y")
    if max(t,st) == t and max(end,t) == end:
        return True
    else:
        return False

def Main():
    print('server starts...')
    client, addr = sock.accept() # addr = (ip,port) , waiting for connection
    while True:
        data = client.recv(1024)
        print('request = %s' %(data))
        if data=="Close":
            break
        args = data.split()
        if not args:
            ls = "Please enter the command"
            # print ls
            client.send(ls)
        elif args[0]== "index":
            if len(args) == 1:
                temp = os.popen('ls').read().split()
                ls = "\n".join(temp)
            elif args[1] == "longlist" :
                files = os.popen('ls').read().split()
                lis = []
                for it in range(len(files)):
                    siz = os.stat(files[it]).st_size
                    d = os.path.isdir(files[it])
                    if d == True:
                        typ = "Directory"
                    else:
                        typ = "File     "
                    ts = get_mtime(files[it])
                    lis.append(files[it] + " " + str(siz) +" "+ str(ts) + " " + typ)
                    ls = "\n".join(lis)
            elif args[1] == "shortlist" and len(args) == 12 :
                st = args[2]+" "+args[3]+" "+args[4]+" "+args[5]+" "+args[6]
                end = args[7]+" "+args[8]+" "+args[9]+" "+args[10]+" "+args[11]
                files = os.popen('ls').read().split()
                lis = []
                for it in range(len(files)):
                    siz = os.stat(files[it]).st_size
                    d = os.path.isdir(files[it])
                    if d == True:
                        typ = "Directory"
                    else:
                        typ = "File     "
                    ts = get_mtime(files[it])
                    if check_time(ts,st,end):
                        lis.append(files[it] + " " + str(siz) +" "+ str(ts) + " " + typ)
                    ls = "\n".join(lis)
            elif args[1] == "regex" and len(args) == 3:
                comm = "ls | grep " + args[2] + " ";
                status, output = commands.getstatusoutput(comm)
                # print output
                ls = output
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
                    ck = hashlib.md5(open(args[2], 'rb').read()).hexdigest()
                    ts = get_mtime(args[2])
                    ck = ck +" "+ ts
            elif args[1] == "checkall":
                files = os.popen('ls').read().split()
                for it in range(len(files)):
                    ck = hashlib.md5(open(files[it], 'rb').read()).hexdigest()
                    ts = get_mtime(files[it])
                    files[it] = files[it] + " " + ck +" "+ts
                ck = "\n".join(files)
            else:
                ck = "please check the syntax"
            client.send(ck)
        elif args[0] == "download" and len(args)==3:
            if os.path.isfile(args[2]):
                client.send("Exist")
            else:
                client.send("Not Exist")
            if os.path.isfile(args[2]):
                if args[1] == "TCP":
                    with open(args[2]) as fileobject:
                        for line in fileobject:
                            client.send(line)
                    time.sleep(1)
                    client.send("zqqxq")

                elif args[1] == "UDP":
                    with open(args[2]) as fileobject:
                        for line in fileobject:
                            sockudp.sendto(line, (hostudp, portudp))
                            # print "data s= ", line
                    time.sleep(1)
                    var = "zqqxq" + hashlib.md5(open(args[2], 'rb').read()).hexdigest()
                    sockudp.sendto(var, (hostudp, portudp))
                else:
                    ls = "Enter TCP or UDP as second argument"
                    client.send(ls)
        else:
            ls = "Please check command or Format"
            client.send(ls)
    client.close()
    sockudp.close()
    print('connection closed, Bye!')


if __name__ == "__main__":
    Main()
    sock.shutdown(socket.SHUT_RDWR)
