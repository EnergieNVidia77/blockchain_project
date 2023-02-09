"""
@file node.py
@author Toufic Talha
@date 2023-01-21
"""

import sys
import threading
from node_class import Node

my_ip = sys.argv[1]
my_port = int(sys.argv[2])

node = Node(my_ip, my_port)
receive_thread = threading.Thread(target=node.receive, daemon=True)
receive_thread.start()

try :
    target_ip = sys.argv[3]
    target_port = int(sys.argv[4])
    node.connect(target_ip, target_port)
except IndexError:
    print("No target ip or port specified")

while True:
    cmd = input()
    if cmd == 'exit':
        node.close_connections()
        break

