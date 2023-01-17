import threading
import sys
import socket
import uuid


class Miner:

    def __init__(self, host, port):
        self.sock_recv_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock_recv_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_recv_conn.bind((host, port))
        self.sock_recv_conn.listen()
        print(f"Listening on {port}")
        self.uuid = str(uuid.uuid4())
        print(f"My uuid {self.uuid}")
        self.clients = {}

    def handle_client(self, conn):
        while True:
            data = conn.recv(1024).decode()
            print(data)

    
    def receive(self):
        while True:
            conn, addr =  self.sock_recv_conn.accept()
            print("Connected with a client")
            other_uuid = conn.recv(1024).decode()
            self.clients[other_uuid] = conn
            print(self.clients)
            conn.send(self.uuid.encode())
            conn_thread = threading.Thread(target=self.handle_client, args=(conn,))
            conn_thread.start()

    def connect(self, host, port):
        sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock_emit_conn.connect((host, port))
        print(f"Connected to {port}")
        sock_emit_conn.send(self.uuid.encode())
        other_uuid = sock_emit_conn.recv(1024).decode()
        self.clients[other_uuid] = sock_emit_conn
        print(self.clients)
