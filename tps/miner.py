import threading
import sys
import socket
import uuid

sock_recv_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock_recv_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock_emit_conn = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock_emit_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

my_uuid = uuid.uuid4()
print(my_uuid)

my_ip = sys.argv[1]
my_port = sys.argv[2]

my_addr = (my_ip, int(my_port))
sock_recv_conn.bind(my_addr)
sock_recv_conn.listen()

users_list = {}
users_thread = {}

try:
    target_ip = sys.argv[3]
    target_port = sys.argv[4]
except IndexError:
    print("Miner A")

def listenMsg(id):
    while(True):
        data = users_list[id].recv(1024).decode()
        data = data.split()
        if not data[0] in users_list:
            users_list[data[0]] = data[1]
            print(users_list)

def addTolist(id, conn):
    users_list[id] = conn
    t = threading.Thread(target= listenMsg)
    users_thread[id] = t

def connect():
    while True:
        conn, addr = sock_recv_conn.accept()
        data = conn.recv(1024).decode()
        addTolist(data, conn)
        print(data)
        print(users_list)
        data_to_send = str(my_uuid)
        conn.send(data_to_send.encode())
        for user in users_list:
            print(user)
            data = str(conn)
            users_list[user].send(data.encode())
            str_user = str(users_list[user])
            conn.send(str_user.encode())
        print(users_list)


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
        data = str(my_uuid)
        sock_emit_conn.send(data.encode())
        data_recv = sock_emit_conn.recv(1024).decode()
        addTolist(data_recv, sock_emit_conn)
        print(data_recv)
        #print(users_list)




    except NameError:
        print("No target addr or target port defined")


if __name__ == '__main__':
    main()