import wallet_class as wc
import sys

my_ip = sys.argv[1]
my_port = int(sys.argv[2])
miner_port = int(sys.argv[3])


wall = wc.Wallet(my_ip, my_port, miner_port)
while True :
	msg = input()
	msg_array = msg.split()
	if msg_array[0] == "/transac":
		wall.send_transaction(msg)
