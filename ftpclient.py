#!/usr/bin/env python3

import socket
import time
import os

servsocket = socket.socket()
servsocket.settimeout(3)
bash = ""
connected = False

while True:

    #input from user split by spaces
    val = input(bash + "$>")
    words = val.split()

    #no input
    if(not val):
        continue

    #manual usage
    if(words[0] == "MAN"):
        print("CONNECT <ip> <port>\t\t\tconnect to server")
        print("LIST\t\t\t\t\tlists files on server")
        print("LS\t\t\t\t\tlist local files")
        print("RETRIEVE <serverfile> <localfile>\tgets file from server")
        print("STORE <localfile> <serverfile>\t\tsends local file to server")
        print("QUIT\t\t\t\t\tends session")

    #Connect to server with ip and port if not already connected
    if(words[0] == "CONNECT"):
        if(connected):
            print("...Already Connected...")
            continue
        print("Connecting...")
        success = servsocket.connect_ex((words[1],int(words[2])))
        if(success == 0):
            print("...Connected to Server...")
            connected = True
            bash = "(" + words[1] + ")"
        else:
            print("...Error Connecting To Server...")
            servsocket = socket.socket()
            servsocket.settimeout(3)

    #Request list of files from server
    if(words[0] == "LIST"):
        if(not connected):
            print("...Not connected to server...")
            continue
        print("...Listing Server Files...")
        servsocket.send("LIST".encode())
        msg = servsocket.recv(1024).decode()
        files = msg.split(',')
        for f in files:
            print(f)

    #List local files
    if(words[0] == "LS"):
        print("...Listing Local Files...")
        filenames = os.listdir()
        for f in filenames:
            print(f)

    #Retrieve file from server
    #  RETRIEVE <serverfile> <localfile>
    if(words[0] == "RETRIEVE"):
        if(not connected):
            print("...Not connected to server...")
            continue
        print("...Retrieving file from server...")
        servsocket.send(val.encode())
        f = open(words[2],"wb")
        while True:
            data = servsocket.recv(1024)
            if(data == b"DONE"):
                print("...File done downloading...")
                break
            f.write(data)
        print("...File closed...")
        f.close()

    #Store local file on server
    #  STORE <localfile> <serverfile>
    if(words[0] == "STORE"):
        if(not connected):
            print("...Not connected to server...")
            continue
        servsocket.send(val.encode())
        print("...Sending file to server...")
        filetosend = open(words[1],"rb")
        data = filetosend.read(1024)
        while data:
            servsocket.send(data)
            data = filetosend.read(1024)
        filetosend.close()
        print("...File Sent...")
        time.sleep(0.5)
        servsocket.send(b"DONE")

    #End session
    if(words[0] == "QUIT"):
        print("...Quiting...")
        if(connected):
            servsocket.send("QUIT".encode())
            servsocket.close()
        break
