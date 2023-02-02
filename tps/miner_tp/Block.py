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
