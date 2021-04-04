#!/usr/bin/env python3

# Echo server program

import socket, sys, re, os, time
sys.path.append("../lib")       # for params
import params
from sockFrame import frameSock
import Threader

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "threadServer"
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
    Threader.Worker(conn, addr).start() #starts thread
    
    
