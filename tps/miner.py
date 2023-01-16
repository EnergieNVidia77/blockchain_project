import threading
import sys
import socket

sock_accept = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock_accept.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

my_ip = sys.argv[1]
my_port = sys.argv[2]

users_list = {}

try:
    target_ip_addr = sys.argv[3]
    target_port = sys.argv[4]
    print("Miner B")
except IndexError:
    print("Miner A")



def connect():
    while True:
        conn, addr = sock_accept.accept()

def main():

    connect_thread = threading.Thread(target=connect, daemon=True)

    print("My addr: " + my_ip)
    print("My port: " + my_port)

    try :
        print("Target addr: " + target_ip_addr)
        print("Target port: " + target_port)
    except NameError:
        print("No target addr or target port defined")

    return 0


if __name__ == '__main__':
    main()