import threading
import socket
import pickle
import time
from message_class import Message

import ecdsa
from ripemd import ripemd160
import hashlib
import binascii
import base58


class Wallet:

	def __init__(self, address, port, node_port):
		#balance (default 100)
		self.balance = 100
		#node
		self.node = node_port
		#my port
		self.port = port
		#socket
		self.bitcoin_addr = self.gen_addr()
		self.sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		self.sock_emit_conn.connect((address, node_port))
		print(f"Connected to {node_port}")
		msg_to_node = "/wallet_login " + self.bitcoin_addr.decode()
		message = Message(port, node_port, msg_to_node)
		pack_msg = pickle.dumps(message)
		self.sock_emit_conn.send(pack_msg)
		self.handle_connection(self.sock_emit_conn)

	def handle_connection(self, conn):
		rcv_th = threading.Thread(target=self.rcv_transaction, args=(conn,), daemon=True)
		rcv_th.start()

	def send_transaction(self, transaction):
		data = transaction.split()
		msg = Message(self.port, data[1], data[2])
		msg = pickle.dumps(msg)	
		self.sock_emit_conn.send(msg)

	def rcv_transaction(self, conn):
		while True:
			packed_recv_msg = conn.recv(1024)
			if not packed_recv_msg:
				print("No data or connection lost")
				return 
			recv_msg = pickle.loads(packed_recv_msg)
			print(f"{recv_msg}")
			self.msg_analysis(recv_msg)
		
	def msg_analysis(self, msg):
		payload = msg.get_payload()
		data = payload.split()
		if data[0] == "/sucess_log":
			print("Sucessfully connected to network")

	def gen_addr(self):
		ecdsaPrivateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
		print("ECDSA Private Key: ", ecdsaPrivateKey.to_string().hex())
		ecdsaPublicKey = '04' +  ecdsaPrivateKey.get_verifying_key().to_string().hex()
		print("ECDSA Public Key: ", ecdsaPublicKey)
		hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(ecdsaPublicKey)).hexdigest()
		print("SHA256(ECDSA Public Key): ", hash256FromECDSAPublicKey)
		ripemd160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
		print("RIPEMD160(SHA256(ECDSA Public Key)): ", ripemd160FromHash256.hexdigest())
		prependNetworkByte = '00' + ripemd160FromHash256.hexdigest()
		print("Prepend Network Byte to RIDEMP160(SHA256(ECDSA Public Key)): ", prependNetworkByte)
		hash = prependNetworkByte
		for x in range(1,3):
			hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
			print("\t|___>SHA256 #", x, " : ", hash)
		cheksum = hash[:8]
		print("Checksum(first 4 bytes): ", cheksum)
		appendChecksum = prependNetworkByte + cheksum
		print("Append Checksum to RIDEMP160(SHA256(ECDSA Public Key)): ", appendChecksum)
		bitcoinAddress = base58.b58encode(binascii.unhexlify(appendChecksum))
		print("Bitcoin Address: ", bitcoinAddress.decode('utf8'), " ", len(bitcoinAddress))
		return bitcoinAddress