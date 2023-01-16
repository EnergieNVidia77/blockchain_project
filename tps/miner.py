import threading
import sys
import socket

sock_recv_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock_recv_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock_emit_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

my_ip = sys.argv[1]
my_port = sys.argv[2]

my_addr = (my_ip, int(my_port))
sock_recv_conn.bind(my_addr)
sock_recv_conn.listen()

users_list = {}

try:
    target_ip = sys.argv[3]
    target_port = sys.argv[4]
    print("Miner B")
except IndexError:
    print("Miner A")



def connect():
    while True:
        conn, addr = sock_recv_conn.accept()
        data = conn.recv(1024).decode()
        print(data)
        data_to_send = "You have successfully connected to your target"
        conn.send(data_to_send.encode())


def main():

    connection_thread = threading.Thread(target=connect)
    connection_thread.start()

    print("My addr: " + my_ip)
    print("My port: " + my_port)

    try :
        print("Target addr: " + target_ip)
        print("Target port: " + target_port)

        target_addr = (target_ip, int(target_port))
        sock_emit_conn.connect(target_addr)
        data = "Miner B has connected"
        sock_emit_conn.send(data.encode())
        data_recv = sock_emit_conn.recv(1024).decode()
        print(data_recv)


    except NameError:
        print("No target addr or target port defined")


if __name__ == '__main__':
    main()