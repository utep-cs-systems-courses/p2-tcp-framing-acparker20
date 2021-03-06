#! /usr/bin/env python3

# Echo client program
import os, socket, sys, re
sys.path.append("../lib")       # for params
import params
from sockFrame import frameSock 
from read import my_getLine
from read import parseTCPInput

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "frameClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
        print("MADE CONNECTION")
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay'])
if delay != 0:
    print(f"sleeping for {delays}s")
    time.sleep(delay)
    print("Done sleeping")
    

fs = frameSock(s)

input = my_getLine()
command,localfile, host, remotefile = parseTCPInput(input)

print(remotefile)
fs.messagesend(remotefile.encode()) #sending file

responsesvr = fs.messagercv() #receive servers response

if responsesvr == "Incorrect":
    os.write(2, ("File cannot be transferred").encode())
    sys.exit(1)

else: #Correct
    filedir = os.open(localfile, os.O_RDONLY)
    buf = ""
    msg = ""

    while True:
        buf = os.read(filedir, 100) #read 512 bytes
        data = buf.decode()
        if len(data) == 0: #exit if empty data
            break
        msg += data #append data

    fs.messagesend(msg.encode()) #send data as message
    s.close()
        
