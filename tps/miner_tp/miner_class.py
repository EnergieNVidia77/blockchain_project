import threading
import time
import socket
import uuid
import pickle

class Miner:

    def __init__(self, host, port):
        self.sock_recv_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock_recv_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_recv_conn.bind((host, port))
        self.sock_recv_conn.listen()
        print(f"Listening on {port}")
        self.miners = []
        self.connected_miner = []

    def send_my_list(self, conn, list):
        msg_to_send = "/my_tab "
        list_str = ' '.join(str(e) for e in list)
        msg_to_send = msg_to_send + list_str
        packed_msg = pickle.dumps(msg_to_send)
        conn.send(packed_msg)

    def port_msg(self, conn, port):
        self.send_my_list(conn, self.miners)
        self.miners.append(int(port))
        self.connected_miner.append(int(port))
        print(f"My connected miners {self.connected_miner}")
        print(f"Known miner {self.miners}")

    def my_tab_msg(self, conn, list):
        miners_to_connect = []
        for i in range(len(list)):
            if not int(list[i]) in self.miners:
                print(f"Adding {int(list[i])} to connect")
                miners_to_connect.append(int(list[i]))
        for miner in miners_to_connect:
            self.connect("localhost", miner)

    def msg_analysis(self, conn, msg):
        if msg[0] == "/port":
            self.port_msg(conn, msg[1])
        elif msg[0] == "/my_tab":
            list = []
            for i in range(1, len(msg)):
                list.append(msg[i])
            self.my_tab_msg(conn, list)

    def handle_miner(self, conn):
        while True:
            packed_recv_msg = conn.recv(1024)
            if not recv_msg:
                print("No data or connection lost")
                break
            recv_msg = pickle.loads(packed_recv_msg)
            recv_msg = recv_msg.split()
            print(f"I received {recv_msg}")
            self.msg_analysis(conn, recv_msg)

    def receive(self):
        while True:
            conn, addr =  self.sock_recv_conn.accept()
            print(f"Connected with {addr}")
            thread_miner = threading.Thread(target=self.handle_miner, args=(conn,))
            thread_miner.start()
    
    def send_port(self, conn, port):
        msg_to_send = "/port " + str(port)
        pack_msg = pickle.dumps(msg_to_send)
        conn.send(pack_msg)

    def connect(self, host, port):
        sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock_emit_conn.connect((host, port))
        print(f"Connected to {port}")
        self.miners.append(port)
        self.connected_miner.append(port)
        my_addr, my_port = self.sock_recv_conn.getsockname()
        self.send_port(sock_emit_conn, my_port)
        thread_miner = threading.Thread(target=self.handle_miner, args=(sock_emit_conn,))
        thread_miner.start()
        
