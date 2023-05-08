from node_class import Node
from transaction_class import Transaction
from block_class import Block
from blockchain_class import Blockchain
from datetime import datetime as dt
import hashlib
import random as rd
from message_class import Message
import pickle


class Miner(Node):
    def __init__(self, host, port, blockchain):
        super().__init__(host, port)
        self.blockchain = Blockchain()
        self.transactions = []
        self.last_nonce = None

    def print_miner_info(self):
        print("Number of blocks: ", self.blockchain.get_nb_blocks())
        print("Hash of last block: ",
              self.blockchain.get_last_block().get_hash())
        #print("Hash of the previous block:",
              #self.blockchain.get_last_block().get_previous_hash())

        print("Transactions:", self.transactions)

    def mining(self):
        print("Mining block")
        new_Block = Block(self.last_nonce, self.transactions, self.blockchain.get_last_block().get_hash())
        print("Broadcasting the new block")
        self.blockchain.add_block(new_Block)
        self.broadcast(new_Block)
        print(self.transactions)
        for transaction in self.transactions:
            recipient = str.encode(transaction.get_recipient())
            if recipient in self.wallets:
                # create updating message
                wallet_socket = self.wallets[recipient]
                wallet_msg = f"/receiving {transaction.get_amount()}"
                wallet_payload = Message(self.my_port, recipient, wallet_msg)
                packed_msg = pickle.dumps(wallet_payload)
                wallet_socket.send(packed_msg)
            sender = transaction.get_sender()
            print(sender)
            print(type(sender))
            if sender in self.wallets:
                # create updating message
                wallet_socket = self.wallets[sender]
                wallet_msg = f"/paying {transaction.get_amount()}"
                wallet_payload = Message(self.my_port, sender, wallet_msg)
                packed_msg = pickle.dumps(wallet_payload)
                wallet_socket.send(packed_msg)
        self.transactions = []

    # Function used to do the Proof of work
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
                nonce_bytes = nonce.to_bytes(8, byteorder="big")
                last_block_hash = self.blockchain.get_last_block().get_hash().encode("utf-8")
                add_content = self.get_content().encode("utf-8")

                hashed_data = nonce_bytes + last_block_hash + (add_content)

                hashed_result = hashlib.sha256(hashed_data).hexdigest()
                answer = hashed_result[0:difficuly]

                # Here, the miner solved the puzzle
                if answer == difficuly*"5":
                    self.last_nonce = nonce
                    self.mining()
                    break
                nonce = rd.randint(0, 1000000000000000)
                #nonce += 1
        else:
            print("No transaction in the miner pool: Not doing POW")

    # Function called when a new block is received
    def checking_pow(self, transactions, nonce, difficuly=2):
        print("Checking POW")
        nonce_bytes = nonce.to_bytes(8, byteorder="big")
        last_block_hash = self.blockchain.get_last_block().get_hash().encode("utf-8")

        transactions_candidate = transactions
        transactions_candidate.sort(key=lambda x: x.sent_time)
        content = "".join([
            str(t.get_hash()) for t in transactions_candidate
            ]).encode("utf-8")

        hashed_data = nonce_bytes + last_block_hash + (content)
        hashed_result = hashlib.sha256(hashed_data).hexdigest()
        answer = hashed_result[0:difficuly]

        if answer == difficuly*"5":
            print("Valid block!")
            return True
        return False

    def msg_analysis(self, conn, msg):
        payload = msg.get_payload()
        match payload:
            case str():
                # Get the current number of miner connected
                nb_miners_before = len(self.nodes_ports)
                super().msg_analysis(conn, msg)
                # Get the current number of miner ConnectionAbortedError
                # After analysis
                nb_miners = len(self.nodes_ports)

                # Comparing the 2 values, if it is different, it is a miner
                if nb_miners != nb_miners_before:
                    print("New miner!")
                    _, my_port = self.sock_recv_conn.getsockname()
                    dest = self.nodes_ports[-1]
                    # Send the blockchain to the new miner
                    to_send = Message(my_port, dest, self.blockchain)
                    packed_msg = pickle.dumps(to_send)
                    self.nodes_socket_dict[str(dest)].send(packed_msg)

            case bytes():
                return super().msg_analysis(conn, msg)

            case Transaction():
                if payload.get_sender() in self.wallets:
                    self.broadcast(payload)
                self.transactions.append(payload)
                self.transactions.sort(key=lambda x: x.sent_time)

            # Case when a new miner access to the network
            case Blockchain():
                print("Replacing current blockchain with a new one")
                self.blockchain = payload

            case Block():
                print("Block received")
                transactions_candidate = payload.get_transactions()
                nonce_candidate = payload.get_nonce()

                if self.checking_pow(transactions_candidate, nonce_candidate):
                    print("Valid new block received")
                    # Remove all the transactions contained in the new block
                    # from the transaction pull of the miner
                    self.transactions = []

                    # Appending the block in the blockchain
                    self.blockchain.add_block(payload)
                    
                    # check if updated wallet in my dictionnary
                    for transaction in payload.get_transactions():
                        recipient = str.encode(transaction.get_recipient())
                        if recipient in self.wallets:
                            # create updating message
                            wallet_socket = self.wallets[recipient]
                            wallet_msg = f"/receiving {transaction.get_amount()}"
                            wallet_payload = Message(self.my_port, recipient, wallet_msg)
                            packed_msg = pickle.dumps(wallet_payload)
                            wallet_socket.send(packed_msg)
                        sender = transaction.get_sender()
                        print(sender)
                        print(type(sender))
                        if sender in self.wallets:
                            # create updating message
                            wallet_socket = self.wallets[sender]
                            wallet_msg = f"/paying {transaction.get_amount()}"
                            wallet_payload = Message(self.my_port, sender, wallet_msg)
                            packed_msg = pickle.dumps(wallet_payload)
                            wallet_socket.send(packed_msg)
                else:
                    print("Something went wrong")
                    

