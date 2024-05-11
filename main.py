from flask import Flask, jsonify, request, redirect
import requests
import json
import random

from blockchain import Blockchain  # Assuming you have a Blockchain class defined in blockchain.py
from publishsubscribe import PubSub  # Assuming you have a PubSub class defined in publishsubscribe.py

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

DEFAULT_PORT = 3000
ROOT_NODE_ADDRESS = f"http://localhost:{DEFAULT_PORT}"
pubsub.broadcast_chain()

@app.route('/api/blocks', methods=['GET'])
def get_blocks():
    return jsonify(blockchain.chain), 200

@app.route('/api/mine', methods=['POST'])
def mine_block():
    data = request.json.get('data')
    blockchain.add_block(data)
    pubsub.broadcast_chain()
    return redirect('/api/blocks')

def sync_chains():
    response = requests.get(f"{ROOT_NODE_ADDRESS}/api/blocks")
    if response.status_code == 200:
        root_chain = response.json()
        print("Replace chain on sync with", root_chain)
        blockchain.replace_chain(root_chain)

if __name__ == '__main__':
    if bool(os.getenv('GENERATE_PEER_PORT', False)):
        peer_port = DEFAULT_PORT + random.randint(1, 1000)
    else:
        peer_port = DEFAULT_PORT
    port = peer_port
    app.run(port=port)
    print(f"Listening on port {port}")
    sync_chains()
