import time
from config import GENESIS_DATA, MINE_RATE
from crypto_hash import crypto_hash

class Block:
    def __init__(self, timestamp, prevHash, hash, data, nonce, difficulty):
        self.timestamp = timestamp
        self.prevHash = prevHash
        self.hash = hash
        self.data = data
        self.nonce = nonce
        self.difficulty = difficulty

    @staticmethod
    def genesis():
        return Block(**GENESIS_DATA)

    @staticmethod
    def mine_block(prev_block, data):
        prev_hash = prev_block.hash
        timestamp = time.time_ns()
        difficulty = Block.adjust_difficulty(prev_block, timestamp)
        nonce = 0
        while True:
            nonce += 1
            hash = crypto_hash(timestamp, prev_hash, data, nonce, difficulty)
            if hash[:difficulty] == '0' * difficulty:
                break
        return Block(timestamp, prev_hash, hash, data, nonce, difficulty)

    @staticmethod
    def adjust_difficulty(prev_block, timestamp):
        difficulty = prev_block.difficulty
        if difficulty < 1:
            return 1
        difference = timestamp - prev_block.timestamp
        if difference > MINE_RATE:
            return difficulty - 1
        return difficulty + 1

# Usage:
# block1 = Block(hash="0xacb", timestamp="2/03/24", prevHash="0xc12", data="oi_rju", nonce=0, difficulty=1)

# genesis_block = Block.genesis()
# print(genesis_block)

# result = Block.mine_block(bl
