import hashlib
import json
from time import time
from textwrap import dedent
from uuid import uuid4
from flask import Flask

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self, proof, previous_hash = None):
        """
        Creates a new block and adds it to the chain
        :param proof: <int> the proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> hash of previous block
        :return: <dict> new block
        """
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
        # Adds a new transaction to the list of transactions
        """
        生成新交易信息，信息将加入下一个待挖的区块中
        :param sender: <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> amout
        :return: <int> the index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def proof_or_work(self, last_proof):
        """
        简单的工作量证明:
        - 查找一个 p' 使得 hash(pp') 以4个0开头
        - p 是上一个块的证明,  p' 是当前的证明
        :param last_proof: <int>
        :return: <int>
               """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        # Hashes a block, must make sure that the dictionary is ordered, or we'll have inconsistent hashes
        """
        生成快的 SHA-256 hash值
        :param block: <dict> block
        :return: <str>
        """
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last block in the chain
        return self.chain[-1]


# Instantiate our node
app = Flask(__name__)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')
# Instantiate the blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new block"

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route("/chain", methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)










test_block = {
            'index': 1,
            'timestamp': 20180308,
            'transactions': 12345,
            'proof': 100,
            'previous_hash': 6543210,
        }

print("Hello World!")
print(test_block)
print(json.dumps(test_block))
print(json.dumps(test_block, sort_keys = True))
print(json.dumps(test_block, sort_keys = True).encode())

