from flask import Flask, request, jsonify , render_template
import hashlib
import json
import datetime

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash, data=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'data': data  # Include data about students in the block
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


# Create a simple Flask web application
app = Flask(__name__)

# Create a blockchain
blockchain = Blockchain()


# Create an endpoint to add a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    required_fields = ['name', 'age', 'grade']
    if not all(field in data for field in required_fields):
        return 'Missing fields', 400

    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)

    student_data = {
        'name': data['name'],
        'age': data['age'],
        'grade': data['grade']
    }

    block = blockchain.create_block(proof, previous_hash, data=student_data)
    response = {'message': 'Student added successfully!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'student_data': block['data']}
    return jsonify(response), 201


# Create an endpoint to get information about all students
@app.route('/get_students', methods=['GET'])
def get_students():
    student_data = [block['data'] for block in blockchain.chain[1:]]  # Exclude the genesis block
    response = {'students': student_data}
    return jsonify(response), 200

# Create an endpoint to serve the HTML form
@app.route('/add_student_form', methods=['GET'])
def add_student_form():
    return render_template('view_students.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

