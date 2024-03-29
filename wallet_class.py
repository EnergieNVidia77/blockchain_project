import threading
import socket
import pickle
import time
from message_class import Message
from transaction_class import Transaction

import hashlib

import base58
import ecdsa
import binascii


from ripemd import ripemd160
import hashlib
import binascii
import base58


class Wallet:
    def __init__(self, address, port, node_port):
        # bitcoin address
        self.bitcoin_addr = self.gen_addr()
        # balance (default 100)
        self.balance = 100
        self.node = node_port
        self.port = port
        print(f"My bitcoin addr: {self.bitcoin_addr}")
        self.sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock_emit_conn.connect((address, node_port))
        msg_to_node = self.bitcoin_addr
        message = Message(port, node_port, msg_to_node)
        pack_msg = pickle.dumps(message)
        self.sock_emit_conn.send(pack_msg)
        self.handle_connection(self.sock_emit_conn)

    def gen_addr(self):
        ecdsaPrivateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.private_key = ecdsaPrivateKey
        #print("ECDSA Private Key: ", ecdsaPrivateKey.to_string().hex())
        ecdsaPublicKey = '04' + ecdsaPrivateKey.get_verifying_key().to_string().hex()
        self.public_key = ecdsaPublicKey
        #print("ECDSA Public Key: ", ecdsaPublicKey)
        hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(ecdsaPublicKey)).hexdigest()
        # print("SHA256(ECDSA Public Key): ", hash256FromECDSAPublicKey)
        ripemd160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
        # print("RIPEMD160(SHA256(ECDSA Public Key)): ", ripemd160FromHash256.hexdigest())
        prependNetworkByte = '00' + ripemd160FromHash256.hexdigest()
        # print("Prepend Network Byte to RIDEMP160(SHA256(ECDSA Public Key)): ", prependNetworkByte)
        hash = prependNetworkByte
        for x in range(1,3):
            hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
            #print("\t|___>SHA256 #", x, " : ", hash)
        cheksum = hash[:8]
        # print("Checksum(first 4 bytes): ", cheksum)
        appendChecksum = prependNetworkByte + cheksum
        # print("Append Checksum to RIDEMP160(SHA256(ECDSA Public Key)): ", appendChecksum)
        bitcoinAddress = base58.b58encode(binascii.unhexlify(appendChecksum))
        # print("Bitcoin Address: ", bitcoinAddress.decode('utf8'), " ", len(bitcoinAddress))
        return bitcoinAddress

    def handle_connection(self, conn):
        rcv_th = threading.Thread(target=self.rcv_transaction, args=(conn,), daemon=True)
        rcv_th.start()

    def send_transaction(self, operation):
        """
        /transaction bitaddressreceiver amount
        """
        data = operation.split()
        if int(data[2]) <= self.balance:
            transaction = Transaction(self.bitcoin_addr, data[1], data[2])
            msg_to_send = Message(self.bitcoin_addr, data[1], transaction)
            msg = pickle.dumps(msg_to_send)
            self.sock_emit_conn.send(msg)

    def rcv_transaction(self, conn):
        while True:
            packed_recv_msg = conn.recv(4096)
            if not packed_recv_msg:
                print("No data or connection lost")
                return
            recv_msg = pickle.loads(packed_recv_msg)
            print(f"{recv_msg}")
            self.msg_analysis(recv_msg)
    
    def check_transac(self, array_cmd):
        cmd = ' '.join(str(e) for e in array_cmd)
        msg = Message(self.port, self.node, cmd)
        self.sock_emit_conn.send(pickle.dumps(msg))


    def msg_analysis(self, msg):
        payload = msg.get_payload()
        data = payload.split()
        if data[0] == "/sucess_log":
            print("Sucessfully connected to network")
        if data[0] == "/receiving":
            self.increase_balance(data[1])
            self.check_balance()
        if data[0] == "/paying":
            self.decrease_balance(data[1])
            self.check_balance()

    def increase_balance(self, amount):
        self.balance += int(amount)

    def decrease_balance(self, amount):
        self.balance -= int(amount)

    def check_balance(self):
        print(f"current balance : {self.balance}")

    # TODO: List header block, test d'appartenance transaction
