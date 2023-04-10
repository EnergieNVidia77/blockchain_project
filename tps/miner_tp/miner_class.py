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

    def print_miner_info(self):
        print(self.transactions)

    def mining(self):
        new_Block = Block(0, self.transactions, self.blockchain.get_last_block().get_hash())

    def do_proof_of_work(self):
        nonce = 0
        starter = b'Test'
        while True:
            nonce_bytes = nonce.to_bytes(8, byteorder="big")
            hashed_data = nonce_bytes + starter
            hashed_result = hashlib.sha256(hashed_data).digest()

            if hashed_result[0] == 0:
                print("Nonce trouvé : ", nonce)
                break
            nonce += 1
        print(nonce)

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
