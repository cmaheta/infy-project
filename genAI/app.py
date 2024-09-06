from flask import Flask, jsonify
import subprocess
from flask_cors import CORS
from views import views
import secrets

app = Flask(__name__)

#CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.register_blueprint(views, url_prefix="/")
app.secret_key = secrets.token_hex(16)

if __name__ == '__main__':
    app.run(debug=True, port=8080)