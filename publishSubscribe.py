import redis
import json

CHANNELS = {
    'TEST': 'TEST',
    'BLOCKCHAIN': 'BLOCKCHAIN'
}

class PubSub:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.publisher = redis.StrictRedis()
        self.subscriber = redis.StrictRedis()

        self.subscriber.subscribe(**CHANNELS)

        self.subscriber_thread = self.subscriber.pubsub()
        self.subscriber_thread.subscribe(**CHANNELS)
        self.subscriber_thread.run_in_thread(sleep_time=0.001)

        self.subscriber_thread.listen(self.handle_message)

    def handle_message(self, message):
        if message['type'] == 'message':
            channel = message['channel'].decode('utf-8')
            data = json.loads(message['data'].decode('utf-8'))
            
            print(f"Message received. Channel: {channel}, Message: {data}")
            
            if channel == CHANNELS['BLOCKCHAIN']:
                self.blockchain.replace_chain(data)

    def publish(self, channel, message):
        self.publisher.publish(channel, json.dumps(message))

    def broadcast_chain(self):
        self.publish(CHANNELS['BLOCKCHAIN'], self.blockchain.chain)
