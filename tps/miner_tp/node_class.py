"""
@file node_class.py
@author Toufic Talha
@date 2023-01-21
"""

import threading
import socket
import pickle
import time
from message_class import Message

class Node:

    def __init__(self, host, port):
        """__init__ : creates a node object
        Args:
            host (string): ip address of the node
            port (int): listening port of the node
        """
        self.sock_recv_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.sock_recv_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_recv_conn.bind((host, port))
        self.sock_recv_conn.listen()
        print(f"Listening on {port}")
        self.nodes_ports = []
        self.nodes_socket_dict = {}
        self.wallets = {}

    def print_node_info(self):
        """print_node_info : show some info about the node
        """
        print(f"Known node {self.nodes_ports}")
        print(f"My wallets: {self.wallets}")
        print(f"My socket dictionnary: {self.nodes_socket_dict}")

    def close_connections(self):
        """close_connections : close all the connection with other nodes
        """
        addr, sender = self.sock_recv_conn.getsockname()
        data = "/logout " + str(sender)
        for destPort in self.nodes_socket_dict:
            msg = Message(sender, destPort, data)
            self.nodes_socket_dict[destPort].send(pickle.dumps(msg))
            self.nodes_socket_dict[destPort].shutdown(socket.SHUT_RDWR)
            self.nodes_socket_dict[destPort].close()

    def send_my_list(self, conn, list, recipient):
        """send_my_list : sends the list of all know nodes to the newly connected node
        Args:
            conn (socket): socket of the current connection
            list (list): list to send
            recipient (str) : port of the recipient
        """
        my_addr, my_port = self.sock_recv_conn.getsockname()
        command = "/my_tab "
        list_str = ' '.join(str(e) for e in list)
        payload = command + list_str
        msg = Message(my_port, recipient, payload)
        packed_msg = pickle.dumps(msg)
        conn.send(packed_msg)

    def port_msg(self, conn, port):
        """port_msg : add the newly connected node to the know node list 
        Args:
            conn (socket): socket of the current connection
            port (int): port received
        """
        self.send_my_list(conn, self.nodes_ports, port)
        self.nodes_ports.append(int(port))
        self.nodes_socket_dict[port] = conn

    def my_tab_msg(self, list):
        """my_tab_msg : connect to all the nodes that the node I connected to sent me
        Args:
            list (list): list of unknown nodes to connect
        """
        nodes_to_connect = []
        for i in range(len(list)):
            if not int(list[i]) in self.nodes_ports:
                print(f"Adding {int(list[i])} to connect")
                nodes_to_connect.append(int(list[i]))
        for node in nodes_to_connect:
            self.connect("localhost", node)
    
    def logout_node(self,port):
        """logout_node : remove the node that just logged out
        Args:
            port (str): port of the loogged out node
        """
        self.nodes_ports.remove(int(port))
        del self.nodes_socket_dict[port]

    def wallet_login(self, bitcoin_addr, port):
        """wallet_login : register a new wallet
        Args:
            port (str): port of the wallet
        """
        self.wallets[bitcoin_addr] = port

    def broadcast(self, msg):
        """broacast : broadcast a wallet to the network

        Args:
            msg (any type): message to broadcast
        """
        my_addr, my_port = self.sock_recv_conn.getsockname()
        for port in self.nodes_ports:
            payload = Message(my_port, port, msg)
            packed_msg = pickle.dumps(payload)
            self.nodes_socket_dict[str(port)].send(packed_msg)

    def msg_analysis(self, conn, msg):
        """msg_analysis : analyze the incomming message
        Args:
            conn (socket): socket of the current connection
            msg (Message): incomming message
        """
        payload = msg.get_payload()
        match payload:
            case str():
                data = payload.split()
                if data[0] == "/port":
                    self.port_msg(conn, data[1])
                elif data[0] == "/my_tab":
                    list = []
                    for i in range(1, len(data)):
                        list.append(data[i])
                    self.my_tab_msg(list)
                elif data[0] == "/logout":
                    self.logout_node(data[1])
                elif data[0] == "/wallet_login":
                    bitcoin_addr = data[1]
                    self.wallet_login(bitcoin_addr, conn)
                    data = "/sucess_log"
                    addr, port = self.sock_recv_conn.getsockname()
                    my_msg = Message(port, msg.get_sender(), data)
                    conn.send(pickle.dumps(my_msg))
                else:
                    print(data)
            case bytes():
                bitcoin_addr = payload
                self.wallet_login(bitcoin_addr, conn)
                data = "/sucess_log"
                addr, port = self.sock_recv_conn.getsockname()
                my_msg = Message(port, msg.get_sender(), data)
                conn.send(pickle.dumps(my_msg))



    def handle_conn(self, conn):
        """handle_conn : function to handle a connection
        Args:
            conn (socket): socket of the current connection
        """
        while True:
            packed_recv_msg = conn.recv(1024)
            if not packed_recv_msg:
                print("No data or connection lost")
                break
            recv_msg = pickle.loads(packed_recv_msg)
            print(recv_msg)
            self.msg_analysis(conn, recv_msg)

    def receive(self):
        """receive
            Just accept new connections and then creates a thread to handle them
        """
        while True:
            conn, addr =  self.sock_recv_conn.accept()
            #self.nb_recv_conn += 1
            #print(f"Connected with {addr}")
            thread_node = threading.Thread(target=self.handle_conn, args=(conn,), daemon=True)
            thread_node.start()
    
    def send_port(self, conn, sender, recipient):
        """send_port : send the /port command to the node I connected to
        Args:
            conn (socket): socket of the current connection
            port (int): port to send
        """
        data = "/port " + str(sender)
        msg_to_send = Message(sender, recipient, data)
        print(msg_to_send)
        pack_msg = pickle.dumps(msg_to_send)
        conn.send(pack_msg)

    def connect(self, host, port):
        """connect : function to connect to a node
        Args:
            host (string): ip address of the remote target  
            port (int): listening port of the remote target
        """
        sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        sock_emit_conn.connect((host, port))
        self.nodes_ports.append(port)
        self.nodes_socket_dict[str(port)] = sock_emit_conn
        my_addr, my_port = self.sock_recv_conn.getsockname()
        self.send_port(sock_emit_conn, my_port, port)
        thread_node = threading.Thread(target=self.handle_conn, args=(sock_emit_conn,), daemon=True)
        thread_node.start()
