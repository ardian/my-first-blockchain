import hashlib
import json

from time import time
from uuid import uuid4

from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)


    def new_block(self, proof, previous_hash=None):
        # create a new block and add it to the chain
        
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
                
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)

        return block


    def new_transaction(self, sender, recipient, amount):
        # add a new transaction to the list of transactions
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # Create a SHA-256 hash of a Block

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexidigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        pass

    def proof_of_work(self, last_proof):
        # Simple proof of Work Algorithm

        proof = 0 
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof


    @staticmethod
    def valid_proof(last_proof, proof):
        #Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        return guess_hash[:4] == "0000"

# Instantiate the node

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')


# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new block"


@app.route('/transactions/new', methods=[POST])
def new_transaction():
    return "We'll add a new transaction"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {

        'chain': blockchain.chain,
        'length': len(blockchain.chain),

    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)