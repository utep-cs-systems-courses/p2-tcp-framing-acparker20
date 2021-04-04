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

progname = "threadClient"
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

print(localfile)
print(remotefile)
fs.messagesend(remotefile.encode()) #sending file

responsesvr = fs.messagercv() #receive servers response
print(responsesvr)

if responsesvr == "No":
    os.write(2, ("File cannot be transferred").encode())
    
elif responsesvr == 'Ok': #If file is "Ok"
    filedir = os.open(localfile, os.O_RDONLY)
    message = os.read(filedir, 100)
    fs.messagesend(message)
    result = fs.messagercv()
    print(result)
s.close()
        
