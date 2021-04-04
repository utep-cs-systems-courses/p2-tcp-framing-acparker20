class frameSock:
    def __init__(self, connectedSocket):
        self.cs = connectedSocket
        self.buff = "" #buffer prevents buffer overwriting every time
#send the encoded message
    def messagesend(self, message):
        lengthStr = str(len(message)) + ':' #frame
        lengthBA = bytearray(lengthStr, 'utf-8') #encode with utf-8
        message = lengthBA + message #add length
        self.cs.send(message) #send message

    def messagercv(self):
        message = ""
        if self.buff == "":
            self.buff += self.cs.recv(100).decode() #100 bytes of msg into buffer
            left, right = seperate(self.buff) #length, msg
            message += self.buff[left:right]#adding bytes to msg
            self.buff = self.buff[right:]#everything after the msg
        while self.buff: #continue parsing the messages
            left, right = seperate(self.buff)
            if len(self.buff) < right:
                self.buff += self.cs.recv(100).decode()
            else:
                message += self.buff[left:right]
                self.buff = self.buff[right:]
        return message
                
#this method is used to return the indicies of the first and last char of a message, this is used for identification: finds index start and beginning
def seperate(string):
    num = ""
    #checks for multiple digits
    while(string[0].isdigit()):
        num += string[0]
        string = string[1:]


    #checks if numeric
            
    if num.isnumeric():
        left = len(num)+1
        right = int(num) + (len(num)+1)
        return left, right
    else:
        return None
            
    
        
