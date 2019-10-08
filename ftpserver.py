#!/usr/bin/env python3

import socket
import threading
import os
import time

PORT = 13393

def on_new_client(clientsocket,add):

    #string of clients ip add
    (addrstr,_) = add

    while True:

        #message from client split on spaces
        msg = clientsocket.recv(1024).decode()
        if(not msg):
            print(addrstr + ": No message...socket probably closed")
            clientsocket.close()
            break
        words = msg.split()

        #send list of files to client
        if(words[0] == "LIST"):
            print(addrstr + ": Requesting List")
            filenames = os.listdir()
            files = ",".join(filenames)
            clientsocket.send(files.encode())

        #send file to client
        if(words[0] == "RETRIEVE"):
            print(addrstr + ": Sending file to client")
            filetosend = open(words[1],"rb")
            data = filetosend.read(1024)
            while data:
                clientsocket.send(data)
                data = filetosend.read(1024)
            filetosend.close()
            print(addrstr + ": File sent")
            time.sleep(0.5)
            clientsocket.send(b"DONE")

        #recieve file from client
        if(words[0] == "STORE"):
            print(addrstr + ": Storing file from client")
            f = open(words[2],"wb")
            while True:
                data = clientsocket.recv(1024)
                if(data == b"DONE"):
                    print(addrstr + ": File done storing")
                    break
                f.write(data)
            print(addrstr + ": File closed")
            f.close()

        #client quits
        if(words[0] == "QUIT"):
            print(addrstr + ": Quiting")
            break

    clientsocket.close()

#main
def main():
    print("Server started on port {}".format(PORT))

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',PORT))
    s.listen(5)

    while True:
        c,addr = s.accept()
        print("Connection from {}".format(addr))
        x = threading.Thread(target=on_new_client,args=(c,addr))
        x.start()

    s.close()

if __name__ == "__main__":
    main()
