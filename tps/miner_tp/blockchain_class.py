from block_class import Block
import hashlib

class Blockchain():
    def __init__(self):
        genesis_block = Block(None, None, hashlib.sha256(b"Genesis").hexdigest())
        self.blocks = [genesis_block]

    def add_block(self, block):
        self.blocks.append(block)

    def get_sub_blockchain(start, end):
        pass

    def __str__(self):
        res = 20*"-"+"\n"
        res += "Blockchain \n"
        res += f"Number of blocks: {len(self.blocks)}\n"
        res += 20*"-"
        return res

    def get_nb_blocks(self):
        return len(self.blocks)

    def get_last_block(self):
        return self.blocks[-1]

    def get_headers(self):
        return [block.get_header() for block in self.blocks]
