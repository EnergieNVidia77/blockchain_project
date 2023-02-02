import datetime
import random
from Transaction import Transaction
from Block import Block
from Blockchain import Blockchain
from Message import Message

"""
A wrapper class to send message easily between nodes or nodes-wallet
@author: port number of the sender
"""


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
