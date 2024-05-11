from blockchain import Blockchain

blockchain = Blockchain()

blockchain.add_block(data="new data")
print(blockchain.chain[-1])

times = []

for i in range(1000):
    prev_timestamp = blockchain.chain[-1].timestamp

    blockchain.add_block(data=f"block {i}")
    next_block = blockchain.chain[-1]
    next_timestamp = next_block.timestamp

    time_diff = next_timestamp - prev_timestamp

    times.append(time_diff)

    average_time = sum(times) / len
