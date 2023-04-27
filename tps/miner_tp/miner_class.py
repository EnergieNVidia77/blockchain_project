from node_class import Node
from transaction_class import Transaction
from block_class import Block
from blockchain_class import Blockchain
from datetime import datetime as dt
import hashlib
import random as rd

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
            nonce = rd.randint(0, 1000000000000000)
            #nonce = 0
            while True:
                #print(nonce)
                nonce_bytes = nonce.to_bytes(8, byteorder="big")
                hashed_data = nonce_bytes + self.blockchain.get_last_block().get_hash().hexdigest().encode("utf-8") + self.get_content().encode("utf-8")

                hashed_result = hashlib.sha256(hashed_data).hexdigest()
                answer = hashed_result[0:difficuly]

                #print(answer)
                if answer == difficuly*"5":
                    print("Nonce trouvé : ", nonce)
                    self.last_nonce = nonce
                    self.mining()
                    break
                nonce = rd.randint(0, 1000000000000000)
                #nonce += 1
        else:
            print("No transaction in the miner pool: Not doing POW")

    def checking_pow(self, transactions, nonce, difficuly=2):
        nonce_bytes = nonce.to_bytes(8, byteorder="big")
        hashed_transactions = "".join([str(t.get_hash()) for t in transactions])
        hashed_data = nonce_bytes + self.blockchain.get_last_block().get_hash().hexdigest().encode("utf-8") + hashed_transactions.encode("utf-8")

        hashed_result = hashlib.sha256(hashed_data).hexdigest()
        answer = hashed_result[0:difficuly]

        if answer == difficuly*"5":
            return True
        return False

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
            case Block():
                print("Block received")
                if self.checking_pow(payload.get_transactions(), payload.get_nonce()):
                    print("Valid new block received")
                    # Remove all the transactions contained in the new block
                    # from the transaction pull of the miner
                    for t in payload.get_transactions():
                        try:
                            self.transactions.remove(t)
                            print("A transaction was removed from the transaction pull")
                        except ValueError:
                            print("A transaction from the new block was not in the transaction pull")
