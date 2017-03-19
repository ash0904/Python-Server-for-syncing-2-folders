import socket,os,time,sys,subprocess

sock = socket.socket()
host = "127.0.0.1"
port = 60000

sock.bind((host, port))
sock.listen(5) # 5 client concurrently connected

def Main():
    print 'Server listening....'
    client, addr = sock.accept() # addr = (ip,port) , waiting for connection
    l = raw_input("prompt>")
    while (l != "quit"):
       client.send(l) # send client message l
       data = client.recv(1024)
       print data
       l = raw_input("prompt>")
    print('Done sending')
    client.send('Over')
    client.close()

if __name__ == "__main__":
    Main()
