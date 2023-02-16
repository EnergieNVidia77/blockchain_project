import threading
import socket
import pickle
import time
from message_class import Message
from transaction_class import Transaction

import hashlib
from random import randbytes

import Crypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

import base58

class Wallet:

	def __init__(self, address, port, node_port):
		#bitcoin address
		self.bitaddress = self.gen_bitcoin_address()
		print(self.bitaddress)
		#balance (default 100)
		self.balance = 100
		#node
		self.node = node_port
		#my port
		self.port = port
		#socket
		self.sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		self.sock_emit_conn.connect((address, node_port))
		print(f"Connected to {node_port}")
		msg_to_node = "/wallet_login"
		message = Message(port, node_port, msg_to_node)
		pack_msg = pickle.dumps(message)
		self.sock_emit_conn.send(pack_msg)
		self.handle_connection(self.sock_emit_conn)

	def gen_bitcoin_address(self):
		#generate key
		key = RSA.generate(1024) #generate public and private keys
		publickey = key.publickey()
		encryptor = PKCS1_OAEP.new(publickey)
		encrypted = encryptor.encrypt(randbytes(4))
		print(f"encrypted {encrypted}")
		#generate bitcoin address
		bitaddress = hashlib.sha256(encrypted).hexdigest()
		print(f"hash256 {bitaddress}")
		#bitaddress = hashlib.ripemd160(bitaddress.encode('utf-8')).hexdigest()
		#add prefix
		bitaddress = "0x00" + bitaddress
		#change encoding
		bitaddress = base58.b58encode(bitaddress)
		return bitaddress

	def handle_connection(self, conn):
		rcv_th = threading.Thread(target=self.rcv_transaction, args=(conn,), daemon=True)
		rcv_th.start()

	def send_transaction(self, operation):
		"""
		/transaction portreceiver bitaddressreceiver amoutnt
		"""
		data = operation.split()
		transaction = Transaction(self.bitaddress, data[2], data[3])
		msg = Message(self.port, data[1], transaction)
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
