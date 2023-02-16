import threading
import socket
import pickle
import time
from message_class import Message

class Wallet:

	def __init__(self, address, port, node_port):
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
			print(f"I received {recv_msg}")
			self.msg_analysis(recv_msg)
		
	def msg_analysis(self, msg):
		payload = msg.get_payload()
		data = payload.split()
		if data[0] == "/sucess_log":
			print("Sucessfully connected to network")
