from os import read

next = 0
limit = 0

#method calls read to fill buffer one character at a time
def my_getChar():
    global next
    global limit

    if next == limit:
        next = 0
        limit = read(0, 1000)# allocating bytes, upperbound

        if limit == 0:
            return None

    if next < len(limit)-1:#checks upperbound for space
        c = chr(limit[next]) #converts from ASCII to char
        next += 1
        return c
    else:
        return None
# returns the line obtained as a string
def my_getLine():
    global next
    global limit
    line = ""
    char = my_getChar()
    while(char != '' and char != None): #checks for character to append
        line += char
        char = my_getChar()
    next = 0 #reset limit, next after line is finished
    limit = 0
    return line

# splits string into seperate arguments for identification and usage in client
def parseTCPInput(string):
    tokens = string.split()
    command = tokens[0]
    localfile = tokens[1]
    tokens2 = tokens[2].split(':')
    host = tokens2[0]
    remotefile = tokens2[1]

    return command, localfile, host, remotefile
        
