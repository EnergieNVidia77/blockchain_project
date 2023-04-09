"""
@file miner.py
@author Toufic Talha
@date 2023-01-21
"""

import sys
import threading
from blockchain_class import Blockchain
from miner_class import Miner

my_ip = sys.argv[1]
my_port = int(sys.argv[2])

blockchain = Blockchain()

miner = Miner(my_ip, my_port, blockchain)
receive_thread = threading.Thread(target=miner.receive, daemon=True)
receive_thread.start()

try :
    target_ip = sys.argv[3]
    target_port = int(sys.argv[4])
    miner.connect(target_ip, target_port)
except IndexError:
    print("No target ip or port specified")

miner.print_node_info()

while True:
    cmd = input()
    if cmd == 'exit':
        miner.close_connections()
        break
    if cmd == 'node info':
        miner.print_node_info()
    if cmd == 'miner info':
        miner.print_miner_info()

