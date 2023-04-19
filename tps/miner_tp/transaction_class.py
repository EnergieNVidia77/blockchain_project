import datetime
import hashlib
import pickle


class Transaction:
    def __init__(self, sender, recipient, amount):
        #self.sequence_number = sequence_number
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.sent_time = datetime.datetime.now()

    def get_sender(self):
        return self.sender

    def get_recipient(self):
        return self.recipient

    def get_amount(self):
        return self.amount

    def get_hash(self):
        content = (self.sender.decode("utf-8") + self.recipient + str(self.amount)).encode("utf-8")
        content = hashlib.sha256(pickle.dumps(content))
        return content

    def formatted_time(self):
        return self.sent_time.strftime("%m/%d/%Y, %H:%M:%S")

    def __str__(self):
        res = 20*"-"+"\n"
        res += f"Transaction from {self.sender} to {self.recipient} at {self.formatted_time()}\n"
        res += f"Amount: {self.amount}\n"
        res += 20*"-"
        return res
