#!/usr/bin/env python3

# Echo server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params
from sockFrame import frameSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #listener socket
s.bind((listenAddr, listenPort))#bind addr and listener port, assigned to sock 
s.listen(1)  # allow only one outstanding request
# ListenerSocket is a factory for connected sockets



while True:
    
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    fs = frameSock(conn)

    
    if os.fork()==0: #in child process, if greater than zero, in parent process

        msgContent = (fs.messagercv())#receive command from client
        print(msgContent)
        filename = msgContent
        print(filename)

        if os.path.isfile(filename): #check for duplicate file
            fs.messagesend(b"Incorrect")
            conn.shutdown(socket.SHUT_WR)
        else:
            fs.messagesend(b"Correct")

        filedir = os.open(filename, os.O_CREAT | os.O_WRONLY) #open and write into file
        os.write(filedir, fs.messagercv().encode())
        os.close(filedir)
