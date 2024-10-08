from flask import Flask, jsonify
from postgreService.Db import Postgres

app = Flask(__name__)

@app.route('/connect', methods=['GET'])
def connect_db():
    connection = Postgres.connect()
    if connection:
        return jsonify({"status": "success", "message": "Connected to database"}), 200
    else:
        return jsonify({"status": "failure", "message": "Failed to connect to database"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)  
