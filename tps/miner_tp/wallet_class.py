import threading
import socket
import pickle
import time

class Wallet:

	def __init__(self, address, host, Mport):
		#balance (default 100)
		self.balance = 100
		#miner
		self.miner = Mport
		# adress
		self.address = address
		#socket
		self.sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		self.sock_emit_conn.connect((address, Mport))
		print(f"Connected to {Mport}")
		print(f"emit socket : {self.sock_emit_conn}")
		msg_to_miner = "/wallet_login " + str(host)
		pack_msg = pickle.dumps(msg_to_miner)
		self.sock_emit_conn.send(pack_msg)
		self.handle_connection(self.sock_emit_conn)

	def handle_connection(self, con):
		rcv_th = threading.Thread(target=self.rcv_transaction, args=(con,), daemon=True)
		rcv_th.start()

	def send_transaction(self, msg):
		msg = pickle.dumps(msg)	
		self.sock_emit_conn.send(msg)

	def rcv_transaction(self, conn):
		while True:
			packed_recv_msg = conn.recv(1024)
			print(f"msg {packed_recv_msg}")
			if not packed_recv_msg:
				print("No data or connection lost")
				return 
			recv_msg = pickle.loads(packed_recv_msg)
			recv_msg = recv_msg.split()
			print(f"I received {recv_msg}")
			#self.msg_analysis(recv_msg)

	def msg_analysis(self, msg):
		msg = msg.split()
		if msg[0] == "/success":
			amount = int(msg[1])
			self.balance -= amount
		
