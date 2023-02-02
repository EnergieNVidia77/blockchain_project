import datetime
import random

class Block():
    def __init__(self,ounce,transactions,previous_block_hash):
        self.previous_block_hash = previous_block_hash
        self.ounce = ounce
        self.transactions = transactions

    def add_transaction(self,transaction):
        self.transactions.append(transaction)

    def get_header(self):
        res = [transaction.get_hash() for transaction in self.transactions]
        return res

    def __str__(self):
        res = 20*"-"+"\n"
        res+="Block\n"
        res+=f"Hash of the previous block: {self.previous_block_hash}\n"
        res+=f"Hash of this block: {self.get_hash()}\n"
        res+=f"ounce: {self.ounce}\n"
        res+=f"Number of transactions: {len(self.transactions)}\nList of transactions:\n"

        for t in self.transactions:
            res+=str(hash(t)) + "\n"
        res+= 20*"-"
        return res

    def get_hash(self):
        return hash(self)

    def have_transactions(self):
        if len(self.transactions) == 0:
            return False
        else:
            return True

class Blockchain():
    def __init__(self):
        self.blocks = []

    def add_block(self,block):
        self.blocks.append(block)

    def get_sub_blockchain(start,end):
        pass

    def __str__(self):
        res = 20*"-"+"\n"
        res+="Blockchain \n"
        res+=f"Number of blocks: {len(self.blocks)}\n"
        res+= 20*"-"
        return res

    def get_nb_blocks(self):
        return len(self.blocks)

    def get_last_block(self):
        return self.blocks[-1]

    def get_headers(self):
        return [block.get_header() for block in self.blocks]
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

    def get_payload():
        return self.payload

    def get_time():
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

        return res

"""
Dummy class, waiting for Jing's part'

class Transaction():
    def __init__(self,sender,receiver,amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def get_hash(self):
        return hash(self)
"""



#Testing purposes
if __name__ == "__main__":
    print("Testing the Message class")
    m1 = Message("a","b","c")
    m2 = m1

    print(m1,m2)

    print("The following should be true: ", m1 == m2)

    print("Testing the Block and Transaction classes")

    bc = Blockchain()
    print("Init")
    print(bc)
    ls = ["a","b","c"]
    rs = ["d","e","f"]
    prev_hash = None
    for s in ls :
        li = []
        for r in rs:
            li.append(Transaction(s,r,s+r))
        o = s + "".join(rs)
        if bc.get_nb_blocks() == 0:
            prev_hash = None
        else:
            prev_hash = hash(bc.get_last_block())
        block = Block(o,li,prev_hash)
        #block.add_transaction(Transaction())
        print(block)
        bc.add_block(block)
    print("End:")
    print(bc)
    print("Headers of all the blocks")
    print(bc.get_headers())
