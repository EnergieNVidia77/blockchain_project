import merkle_class as mC
import hashlib
import pickle
from transaction_class import Transaction

class Block():
    def __init__(self, nonce, transactions, previous_block_hash):
        self.previous_block_hash = previous_block_hash
        self.nonce = nonce
        self.transactions = transactions

        try:
            self.hashList = [transaction.get_hash() for transaction in self.transactions]
        except TypeError:       # When generating Genesis
            print("Creating Genesis")
            self.transactions = [Transaction(b"Origin","Origin",100)]
            self.hashList = [transaction.get_hash() for transaction in self.transactions]

        self.header = mC.makeMerkle(self.hashList)

    # revoir l'arbre de merkel cree a partir de la liste de hash des transaction
    def get_header(self):
        return self.header

    def __str__(self):
        res = 20*"-"+"\n"
        res += "Block\n"
        res += f"Hash of the previous block: {self.previous_block_hash}\n"
        #res += f"Hash of this block: {self.get_hash()}\n"
        res += f"nonce: {self.nonce}\n"
        res += f"Number of transactions: {len(self.transactions)}\nList of transactions:\n"

        for t in self.transactions:
            res += str(t.get_hash()) + "\n"
        res += 20*"-"
        return res

    # revoie le hash du block
    def get_hash(self):
        bytes_block = pickle.dumps(self.__str__())
        return hashlib.sha256(bytes_block)

    # return true si l'arbre contient des transaction faux sinon
    def have_transactions(self):
        if len(self.transactions) == 0:
            return False
        else:
            return True
