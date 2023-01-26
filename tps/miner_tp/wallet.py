import threading
import socket
import pickle
import time

class Wallet:

	def __init__(self, host, Mport, address):
		#balance (default 100)
		self.balance = 100
		#miner
		self.miner = Mport
		# adress
		self.address = address
		#socket
		sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		sock_emit_conn.connect((host, port))
		print(f"Connected to {port}")
		msg_to_miner = "/wallet_login " + self.address
		pack_msg = pickle.dumps(msg_to_miner)
		sock_emit_conn.send(pack_msg)
		handle_connection(sock_emit)

	def handle_connection(con):
		snd_th = threading.Thread(target=self.send_transaction, args=(con,), daemon=True)
		rcv_th = threading.Thread(target=self.rcv_transaction, args=(con,), daemon=True)
		snd_th.start() ; rcv_th.start()

	def send_transaction(con):
		while True:
			msg = input()
			msg = msg.split()
			if msg[0] = "/transac":
				rcvr = msg[1]
				amount = msg[-1]
			
	def rcv_transaction()
		while True:
		    packed_recv_msg = conn.recv(1024)
		    if not packed_recv_msg:
			print("No data or connection lost")
			break
		    recv_msg = pickle.loads(packed_recv_msg)
		    recv_msg = recv_msg.split()
		    #print(f"I received {recv_msg}")
		    self.msg_analysis(recv_msg)

	def msg_analysis(msg):
		msg = msg.split()
		if msg[0] == "/success":
			amount = int(msg[1])
			self.balance -= amount
