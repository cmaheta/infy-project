from flask import Flask, jsonify
import subprocess
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/run-script')
def run_script():
    result = subprocess.run(['python', 'python_script.py'], capture_output=True, text=True)
    return jsonify({'output': result.stdout})

if __name__ == '__main__':
    app.run()