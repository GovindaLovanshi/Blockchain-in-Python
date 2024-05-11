from block import Block
from crypto_hash import crypto_hash

class Blockchain:
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        new_block = Block.mine_block(self.chain[-1], data)
        self.chain.append(new_block)

    def replace_chain(self, chain):
        if len(chain) <= len(self.chain):
            print("The incoming chain is not longer")
            return
        if not Blockchain.is_valid_chain(chain):
            print("The incoming chain is not valid")
            return
        self.chain = chain

    @staticmethod
    def is_valid_chain(chain):
        if chain[0] != Block.genesis():
            return False
        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]

            if block['prevHash'] != last_block.hash:
                return False

            if block['hash'] != crypto_hash(block['timestamp'], block['prevHash'], block['nonce'], block['difficulty'], block['data']):
                return False

            if abs(last_block['difficulty'] - block['difficulty']) > 1:
                return False

        return True

# Usage:
# blockchain = Blockchain()
# blockchain.add_block("Block1")
# blockchain.add_block("Block2")
# result = Blockchain.is_valid_chain(blockchain.chain)
# print(blockchain.chain)
# print(result)
