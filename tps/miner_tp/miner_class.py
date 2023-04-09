from node_class import Node
from transaction_class import Transaction
from block_class import Block
from blockchain_class import Blockchain
class Miner(Node):

    def __init__(self, host, port, blockchain):
        super().__init__(host, port)
        self.blockchain = Blockchain()
        self.transactions = []
    
    def print_miner_info(self):
        print(self.transactions)

    def mining(self):
        new_Block = Block(0, self.transactions, self.blockchain.get_last_block().get_hash())
    
    def msg_analysis(self, conn, msg):
        payload = msg.get_payload()
        match payload:
            case str():
                return super().msg_analysis(conn, msg)
            case bytes():
                return super().msg_analysis(conn, msg)
            case Transaction():
                if payload.get_sender() in self.wallets:
                    self.broadcast(payload)
                self.transactions.append(payload)
                if len(self.transactions) == 2:
                    self.mining()
