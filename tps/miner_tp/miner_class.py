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
        self.uuid = str(uuid.uuid4())
        print(f"My uuid {self.uuid}")
        self.miners = {}
        self.connected_miners = []
        #self.miners[self.uuid] = port

    def handle_initial_exchange(self, conn, flag):
        while True:
            recv_msg = conn.recv(1024).decode()
            if not recv_msg:
                print("No data or connection lost")
                break
            array_recv_msg = recv_msg.split()
            print(f"Miner's uuid {array_recv_msg[0]} and miner's listening port {array_recv_msg[1]}")
            if not array_recv_msg[0] in self.miners:
                self.miners[array_recv_msg[0]] = array_recv_msg[1]
                print(self.miners)
            if flag:
                self.send_info(conn)
                time.sleep(0.5)
                for miner in self.miners:
                    if miner != array_recv_msg[0]:
                        msg_to_send = miner + " " + self.miners[miner]
                        print(msg_to_send)
                        conn.send(msg_to_send.encode())
            else:
                print(array_recv_msg[0])
                print(array_recv_msg[1])
                if not int(array_recv_msg[1]) in self.connected_miners:
                    self.connect('127.0.0.1', int(array_recv_msg[1]))

    def receive(self):
        while True:
            conn, addr =  self.sock_recv_conn.accept()
            print(f"Connected with {addr}")
            recv_thread = threading.Thread(target=self.handle_initial_exchange, args=(conn, 1))
            recv_thread.start()
    
    def send_info(self, conn):
        recv_addr = self.sock_recv_conn.getsockname()
        all_info = self.uuid + " " + str(recv_addr[1])
        encoded_info = all_info.encode()
        conn.send(encoded_info)

    def connect(self, host, port):
        sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock_emit_conn.connect((host, port))
        print(f"Connected to {port}")
        self.connected_miners.append(port)
        self.send_info(sock_emit_conn)
        recv_thread = threading.Thread(target=self.handle_initial_exchange, args=(sock_emit_conn, 0))
        recv_thread.start()
