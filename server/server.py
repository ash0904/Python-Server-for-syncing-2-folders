import socket,os,time,commands,sys,subprocess
import datetime
import hashlib
from threading import Thread

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
def index_func(args):
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
        ls = output
    else:
        ls = "please check the syntax"
    return ls

def hash_func(args):
    if len(args) < 2:
        ck = "please provide arguments"
    elif args[1] == "verify":
        if not args[2]:
            ck = "Enter File name"
        else:
            ck = hashlib.md5(open(args[2], 'rb').read()).hexdigest()
            ts = get_mtime(args[2])
            ck = args[2] + " " + ck +" "+ ts
    elif args[1] == "checkall":
        files = os.popen('ls').read().split()
        for it in range(len(files)):
            ck = hashlib.md5(open(files[it], 'rb').read()).hexdigest()
            ts = get_mtime(files[it])
            files[it] = files[it] + " " + ck +" "+ts
        ck = "\n".join(files)
    else:
        ck = "please check the syntax"
    return ck

def download_func(args,client,portudpi):
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
                    sockudp.sendto(line, (host, portudpi))
                    # print "data s= ", line
            time.sleep(1)
            var = "zqqxq" + hashlib.md5(open(args[2], 'rb').read()).hexdigest()
            sockudp.sendto(var, (host, portudp))
        else:
            ls = "Enter TCP or UDP as second argument"
            client.send(ls)

def sync(client,portudp):
    temp = os.listdir(os.curdir)
    for f in temp:
        comm = "hash verify "+f
        a = comm.split()
        det = hash_func(a)
        client.send(det)
        info = client.recv(1024)
        if info == "download":
            info = info + " TCP " + f
            args = info.split()
            download_func(args,client,portudp)
    time.sleep(1)
    client.send("over")

class ServerThread(Thread):
    def __init__(self, val):
        Thread.__init__(self)
        self.val = val

    def run(self):
        port = 50000
        portudp = 51000
        #TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5) # 5 client concurrently connected

        #UDP socket
        sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        Mains(sock,port,sockudp,portudp)
        sock.shutdown(socket.SHUT_RDWR)

class ClientThread(Thread):
    def __init__(self, val):
        Thread.__init__(self)
        self.val = val

    def run(self):
        #TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 60000
        sock.connect((host, port))

        #UDP socket
        sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        portudp = 61000
        sockudp.bind((host, portudp))

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
            elif l == "sync":
                temp = os.listdir(os.curdir)
                while True:
                    data = sock.recv(1024)
                    if data == "over":
                        break
                    args = data.split()
                    if args[0] not in temp:
                        sock.send("download")
                        if os.path.isfile(args[0]):
                            os.remove(args[0])
                        if sock.recv(1024)  == "Exist":
                            fh = open(args[0], 'a+')
                            while True:
                                data = sock.recv(1024)
                                if data == "zqqxq":
                                    break
                                fh.write(data)
                            fh.close()

                    else:
                        sock.send("present")
                else:
                    print "No such File Exist"
            else:
                data = sock.recv(1024)
                print data
            if l!= "sync":
                l = "sync"
            else:
                l = raw_input("prompt> ")
        sock.send('Close')
        sock.close()
        sockudp.close()


def Mains(sock,port,sockudp,portudp):
    print('server starts...')
    client, addr = sock.accept() # addr = (ip,port) , waiting for connection
    while True:
        data = client.recv(1024)
        # print('request = %s' %(data))
        if data=="Close":
            break
        args = data.split()
        if not args:
            err = "Please enter the command"
            client.send(err)

        elif args[0]== "index":
            ck = index_func(args)
            client.send(ck)

        elif args[0] == "hash":
            ck = hash_func(args)
            client.send(ck)

        elif args[0] == "download" and len(args)==3:
            download_func(args,client,portudp)

        elif args[0] == "sync":
            sync(client,portudp)

        else:
            err = "Please check command or Format"
            client.send(err)
    client.close()
    sockudp.close()


host = "127.0.0.1"
if __name__ == "__main__":

    sthread = ServerThread(1)
    sthread.setName("server")

    cthread = ClientThread(2)
    cthread.setName("client")

    sthread.start()
    time.sleep(5)
    cthread.start()

    sthread.join()
    cthread.join()
    print('connection closed, Bye!')
