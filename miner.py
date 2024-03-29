"""
@file miner.py
@author Toufic Talha
@date 2023-01-21
"""

import sys
import threading
import select
from blockchain_class import Blockchain
from miner_class import Miner

my_ip = sys.argv[1]
my_port = int(sys.argv[2])

blockchain = Blockchain()

miner = Miner(my_ip, my_port, blockchain)
receive_thread = threading.Thread(target=miner.receive, daemon=True)
receive_thread.start()

try:
    target_ip = sys.argv[3]
    target_port = int(sys.argv[4])
    miner.connect(target_ip, target_port)
except IndexError:
    print("No target ip or port specified")

miner.print_node_info()


def user_input():
    while True:
        # With this, we can still interact with the miner console while doing
        # the proof of work
        input_ready, output_ready, except_ready = select.select([sys.stdin], [], [], 0)
        for i in input_ready:
            cmd = i.readline().strip()
            if cmd == 'exit':
                miner.close_connections()
                break
            if cmd == 'node info':
                miner.print_node_info()
            if cmd == 'miner info':
                miner.print_miner_info()
            if cmd == "do_pow":
                proof_of_work_thread = threading.Thread(target=miner.do_proof_of_work)
                proof_of_work_thread.start()


main = threading.Thread(target=user_input)
main.start()
main.join()

