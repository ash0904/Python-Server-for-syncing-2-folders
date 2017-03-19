import socket,os,time,sys,subprocess

sock = socket.socket()
host = "127.0.0.1"
port = 60000

sock.connect((host, port))

def Main():
    while True:
        print('receiving data...')
        data = sock.recv(1024)
        if data=="Over":
            break
        print('msg = %s' %(data))
        args = data.split()
        if args and args[0]== "index":
            if len(args) == 1:
                ls = os.popen('ls').read()
            elif args[1] == "longlist" :
                ls = os.popen('ls -l').read()
            # elif args[1] == "shortlist" :
            #     proc = subprocess.Popen('ls', stdout=subprocess.PIPE)
            #     ls = proc.stdout.read()
            else:
                ls = "please check the syntax"
            sock.send(ls)
        elif args and args[0] == "hash":
            if len(args) < 2:
                ck = "please provide arguments"
            elif args[1] == "verify":
                if not args[2]:
                    ck = "Enter File name"
                else:
                    comm = "cksum " + args[2]
                    ck = os.popen(comm).read()
                # print ck
                sock.send(ck)
        elif args and args[0] == "download":
            with open(args[2]) as fileobject:
                for line in fileobject:
                    sock.send(line)
            time.sleep(1)
            sock.send("zqqx")
    sock.close()
    print('connection closed')

if __name__ == "__main__":
    Main()
