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

    def handle_client(self, conn, flag):
        while True:
            recv_msg_encoded = conn.recv(1024)
            if not recv_msg_encoded:
                print("No data or connection lost")
                break
            recv_msg = pickle.loads(recv_msg_encoded)
            if not recv_msg in self.miners.keys() and type(recv_msg) == str and flag:
                self.miners[recv_msg] = conn
                print(self.miners)
                self.send_uuid(conn)
            elif type(recv_msg) == str:
                self.miners[recv_msg] = conn
                print(self.miners)
            if flag:
                for miner in self.miners:
                    #print(recv_msg[1])
                    if miner != recv_msg and int(recv_msg[1]) < 9000:
                        raddr = self.miners[miner].getpeername() 
                        print(f"I sent this remote {raddr}")
                        packed_raddr = pickle.dumps(raddr)
                        conn.send(packed_raddr)
            elif type(recv_msg) == tuple:
                print(f"Remote I got {recv_msg}")
                print("Trying to connect")
                try:
                    self.connect(recv_msg[0], recv_msg[1])
                except ConnectionRefusedError:
                    print("Connection refused")

    def receive(self):
        while True:
            conn, addr =  self.sock_recv_conn.accept()
            print(f"Connected with {addr}")
            recv_thread = threading.Thread(target=self.handle_client, args=(conn, 1))
            recv_thread.start()
    
    def send_uuid(self, conn):
        encoded_uuid = pickle.dumps(self.uuid)
        conn.send(encoded_uuid)

    def connect(self, host, port):
        sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock_emit_conn.connect((host, port))
        print(f"Connected to {port}")
        self.send_uuid(sock_emit_conn)
        recv_thread = threading.Thread(target=self.handle_client, args=(sock_emit_conn, 0))
        recv_thread.start()
