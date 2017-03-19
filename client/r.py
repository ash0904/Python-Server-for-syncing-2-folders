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
        if args[0]== "index":
            proc = subprocess.Popen('ls', stdout=subprocess.PIPE)
            ls = proc.stdout.read()
            print ls
            sock.send(ls)
    sock.close()
    print('connection closed')

if __name__ == "__main__":
    Main()
