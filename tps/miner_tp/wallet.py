from wallet_class import Wallet
import sys

my_ip = sys.argv[1]
my_port = int(sys.argv[2])
node_port = int(sys.argv[3])

wall = Wallet(my_ip, my_port, node_port)

while True:
    msg = input()
    msg_array = msg.split()
    """
    /transaction bitaddressreceiver amount
    """
    if msg_array[0] == "/transac":
        wall.send_transaction(msg)
    if msg_array[0] == "/balance":
        wall.check_balance()
    if msg_array[0] == "/check":
        wall.check_transac(msg_array);
