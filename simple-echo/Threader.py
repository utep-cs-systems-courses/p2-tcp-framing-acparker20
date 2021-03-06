#! /usr/bin/env python3

import sys,os
import sockFrame
import read
import socket
import threading
from threading import Thread
from time import time


threadNum = 0
currentFile = set()
lock = threading.Lock()

class Worker(Thread):
    def __init__(self, conn, addr):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum);
        threadNum += 1
        self.conn = conn
        self.addr = addr

    def run(self):
        fs = sockFrame.frameSock(self.conn) #establish new framed sock, this was done before in fork and now in thread
    
       # type1 = fs.messagercv() #waits for receives "Send", "Recv" if needed
        filename = fs.messagercv() #recevies name of file beinf written to 
        canTransfer = self.fileTransfer(filename)
        if (canTransfer == False): #check lock
            fs.messagesend(b"wait")
        elif os.path.isfile(filename):
            fs.messagesend(b"No")# file already exist
        else:
            fs.messagesend(b"Ok")
            try: #attempts to write to the file 
                fd = os.open(filename, os.O_CREAT | os.O_WRONLY)
                os.write(fd, fs.messagercv().encode())
                os.close(fd)
                fs.messagesend(b"Writing file") #writes to file if successful
            except:
                fs.messagesend(b"Could not write file")
        self.conn.shutdown(socket.SHUT_WR)

    #Checks if file is already being transferred 
    def fileTransfer(self, filename):
        global currentFile
        global transferLock
        lock.acquire()
        
        if filename in currentFile:
            canTransfer = False
        else:
            canTransfer = True
            currentFile.add(filename)
        lock.release()
        return canTransfer
    # Remove from transfer thread if file is done transferring 
    def endTransfer(self, filename):
        global currentFile
        inTransfer.remove(filename)
        
