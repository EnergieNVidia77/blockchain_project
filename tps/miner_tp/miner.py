"""
@file miner.py
@author Toufic Talha
@date 2023-01-21
"""

import sys
import threading
from miner_class import Miner

my_ip = sys.argv[1]
my_port = int(sys.argv[2])

miner = Miner(my_ip, my_port)
receive_thread = threading.Thread(target=miner.receive)
receive_thread.start()

try :
    target_ip = sys.argv[3]
    target_port = int(sys.argv[4])
    miner.connect(target_ip, target_port)
except IndexError:
    print("No target ip or port specified")


