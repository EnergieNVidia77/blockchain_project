"""
@file miner_class.py
@author Toufic Talha
@date 2023-01-21
"""

import threading
import socket
import pickle
import time

class Miner:

	def __init__(self, host, port):
		"""__init__

		Args:
			host (string): ip address of the miner
			port (int): listening port of the miner
		"""
		self.sock_recv_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		self.sock_recv_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock_recv_conn.bind((host, port))
		self.sock_recv_conn.listen()
		print(f"Listening on {port}")
		self.miners = []
		self.socket_dict = {}
		self.wallets = []
		#self.nb_recv_conn = 0
		#self.nb_send_conn = 0

	def print_miner_info(self):
		print(f"Known miner {self.miners}")
		print(f"My wallets: {self.wallets}")
		#print(f"Current open recv connections: {self.nb_recv_conn}")
		#print(f"Current open emit connections: {self.nb_send_conn}")
		#print("My sockets:")
		#print(self.socket_dict)

	def close_connections(self):
		addr, port = self.sock_recv_conn.getsockname()
		msg = "/logout " + str(port)
		for port in self.socket_dict:
			self.socket_dict[port].send(pickle.dumps(msg))
			self.socket_dict[port].shutdown(socket.SHUT_RDWR)
			self.socket_dict[port].close()

	def send_my_list(self, conn, list):
		"""send_my_list

		Args:
			conn (socket): socket of the current connection
			list (list): list to send
		"""
		msg_to_send = "/my_tab "
		list_str = ' '.join(str(e) for e in list)
		msg_to_send = msg_to_send + list_str
		packed_msg = pickle.dumps(msg_to_send)
		conn.send(packed_msg)

	def port_msg(self, conn, port):
		"""port_msg

		Args:
			conn (socket): socket of the current connection
			port (int): port received
		"""
		self.send_my_list(conn, self.miners)
		self.miners.append(int(port))
		self.socket_dict[port] = conn

	def my_tab_msg(self, list):
		"""my_tab_msg

		Args:
			list (list): list of unknown miners to connect
		"""
		miners_to_connect = []
		for i in range(len(list)):
			if not int(list[i]) in self.miners:
				print(f"Adding {int(list[i])} to connect")
				miners_to_connect.append(int(list[i]))
		for miner in miners_to_connect:
			self.connect("localhost", miner)
	
	def logout_miner(self,port):
		self.miners.remove(int(port))
		del self.socket_dict[str(port)]

	def wallet_login(self, addr):
		self.wallets.append(addr)

	def broadcast(self, msg):
		packed_msg = pickle.dumps(msg)
		for port in self.miners:
			self.socket_dict[str(port)].send(packed_msg)

	def msg_analysis(self, conn, msg):
		"""msg_analysis

		Args:
			conn (socket): socket of the current connection
			msg (array of strings): array of words of the msg received
		"""
		if msg[0] == "/port":
			self.port_msg(conn, msg[1])
		elif msg[0] == "/my_tab":
			list = []
			for i in range(1, len(msg)):
				list.append(msg[i])
			self.my_tab_msg(list)
		elif msg[0] == "/logout":
			self.logout_miner(msg[1])
		elif msg[0] == "/wallet_login":
			self.wallet_login(msg[1])
			snd_msg = pickle.dumps("you loged")
			conn.send(snd_msg)
		elif msg[0] == "/transac":
			print(msg)		
			list = []
			for i in range(1, len(msg)):
				list.append(msg[i])
			self.broadcast(list)
		else:
			print(msg)
		self.print_miner_info()

	def handle_miner(self, conn):
		"""handle_miner

		Args:
			conn (socket): socket of the current connection
		"""
		while True:
			packed_recv_msg = conn.recv(1024)
			if not packed_recv_msg:
				print("No data or connection lost")
				break
			recv_msg = pickle.loads(packed_recv_msg)
			print(f"received : {recv_msg}")
			recv_msg = recv_msg.split()
			#print(f"I received {recv_msg}")
			self.msg_analysis(conn, recv_msg)

	def receive(self):
		"""receive
			Just accept new connections and then creates a thread to handle them
		"""
		while True:
			conn, addr =  self.sock_recv_conn.accept()
			#self.nb_recv_conn += 1
			#print(f"Connected with {addr}")
			thread_miner = threading.Thread(target=self.handle_miner, args=(conn,), daemon=True)
			thread_miner.start()
	
	def send_port(self, conn, port):
		"""send_port

		Args:
			conn (socket): socket of the current connection
			port (int): port to send
		"""
		msg_to_send = "/port " + str(port)
		pack_msg = pickle.dumps(msg_to_send)
		conn.send(pack_msg)

	def connect(self, host, port):
		"""connect

		Args:
			host (string): ip address of the remote target  
			port (int): listening port of the remote target
		"""
		sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
		sock_emit_conn.connect((host, port))
		#print(f"Connected to {port}")
		#self.nb_send_conn += 1
		self.miners.append(port)
		self.socket_dict[port] = sock_emit_conn
		my_addr, my_port = self.sock_recv_conn.getsockname()
		self.send_port(sock_emit_conn, my_port)
		thread_miner = threading.Thread(target=self.handle_miner, args=(sock_emit_conn,), daemon=True)
		thread_miner.start()
