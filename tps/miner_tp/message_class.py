import datetime
"""
A wrapper class to send message easily between nodes or nodes-wallet
@author: port number of the sender
"""
class Message():
    def __init__(self,sender,recipient,payload):
        self.sender = sender
        self.recipient = recipient
        self.payload = payload
        self.sent_time = datetime.datetime.now()


    def get_sender(self):
        return self.sender

    def get_recipient(self):
        return self.recipient

    def get_payload(self):
        return self.payload

    def get_time(self):
        return self.sent_time

    def __equal__(self,other):
        c1 = self.sender == other.sender
        c2 = self.recpient == other.recipient
        c3 = self.payload == other.payload

        return c3 and c2 and c1

    def formatted_time(self):
        return self.sent_time.strftime("%m/%d/%Y, %H:%M:%S")

    def __str__(self):
        res = 20*"-"+"\n"
        res+= f"Message from {self.sender} to {self.recipient} at {self.formatted_time()}\n"
        res+= f"Payload:\n"
        res+=str(self.payload)+"\n"
        res+=20*"-"
