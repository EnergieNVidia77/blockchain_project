import merkelClass as mC
class Block():
    def __init__(self,ounce,transactions,previous_block_hash):
        self.previous_block_hash = previous_block_hash
        self.ounce = ounce
        self.transactions = transactions
    #revoir l'arbre de merkel cree a partir de la liste de hash des transaction
    def get_header(self):
        hashList = [transaction.get_hash() for transaction in self.transactions]
        res = mC.makeMerkel(hashList)
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

    #revoie le hash du block
    def get_hash(self):
        return hash(self)

    #return true si l'arbre contient des transaction faux sinon 
    def have_transactions(self):
        if len(self.transactions) == 0:
            return False
        else:
            return True
