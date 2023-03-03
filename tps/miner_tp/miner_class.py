from node_class import Node


class Miner(Node):

    def __init__(self, host, port, blockchain):
        super().__init__(host, port)
        self.blockchain = blockchain
        self.transactions = []
    