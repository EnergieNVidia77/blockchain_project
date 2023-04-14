import datetime
import hashlib


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
        return hashlib.sha256(self)

    def formatted_time(self):
        return self.sent_time.strftime("%m/%d/%Y, %H:%M:%S")

    def __str__(self):
        res = 20*"-"+"\n"
        res += f"Transaction from {self.sender} to {self.recipient} at {self.formatted_time()}\n"
        res += f"Amount: {self.amount}\n"
        res += 20*"-"
        return res
