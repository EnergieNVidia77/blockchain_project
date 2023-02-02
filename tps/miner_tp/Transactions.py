class Transaction:

    #sender:debiteur, recipient:emitteur
    def __init__(self, sequence_number, sender, recipient, amount):
      self.sequence_number = sequence_number
      self.sender = sender
      self.recipient = recipient
      self.amount = amount

    def get_sender(self):
        return self.sender

    def get_recipient(self):
        return self.recipient

    def get_amount(self):
        return self.amount

    def print_info(self):
        print('%s: %s, %s, %s' % (self.sequence_number, self.sender, self.recipient, self.amount))
