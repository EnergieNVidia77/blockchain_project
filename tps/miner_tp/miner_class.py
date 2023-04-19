from node_class import Node
from transaction_class import Transaction
from block_class import Block
from blockchain_class import Blockchain
from datetime import datetime as dt
import hashlib


class Miner(Node):
    def __init__(self, host, port, blockchain):
        super().__init__(host, port)
        self.blockchain = Blockchain()
        self.transactions = []

        self.last_nonce = None

    def print_miner_info(self):
        print(self.transactions)

    def mining(self):
        print("Mining block")
        new_Block = Block(self.last_nonce, self.transactions, self.blockchain.get_last_block().get_hash())
        print("Broadcasting the new block")
        self.blockchain.add_block(new_Block)
        self.broadcast(new_Block)
        self.transactions = []

    def get_content(self):
        if len(self.transactions) == 0:
            return None
        else:
            m = "".join([str(t.get_hash()) for t in self.transactions])
            return m

    def do_proof_of_work(self, difficuly=2):
        print("Starting to find a nonce")
        if self.get_content() is not None:
            nonce = 0
            starter = b'Test'
            while True:
                nonce_bytes = nonce.to_bytes(8, byteorder="big")
                hashed_data = nonce_bytes + starter + self.blockchain.get_last_block().get_hash().hexdigest().encode("utf-8")
                hashed_result = hashlib.sha256(hashed_data).hexdigest()
                answer = hashed_result[0:difficuly]
                #print(answer)
                if answer == difficuly*"5":
                    print("Nonce trouvé : ", nonce)
                    self.last_nonce = nonce
                    self.mining()
                    break
                nonce += 1
        else:
            print("No transaction in the miner pool: Not doing POW")

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
