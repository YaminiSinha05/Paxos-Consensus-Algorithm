import os
import random
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

NODE_ID = os.getenv("NODE_ID", "1")
PEERS = os.getenv("PEERS", "").split(",")

promises = {}
accepted_values = {}

@app.route("/prepare", methods=["POST"])
def prepare():
    proposal_id = request.json["proposal_id"]
    if proposal_id not in promises or proposal_id > promises[proposal_id]:
        promises[proposal_id] = proposal_id
        return jsonify({"status": "PROMISE", "proposal_id": proposal_id})
    return jsonify({"status": "REJECT", "proposal_id": proposal_id})

@app.route("/accept", methods=["POST"])
def accept():
    proposal_id = request.json["proposal_id"]
    value = request.json["value"]

    if proposal_id in promises:
        accepted_values[proposal_id] = value
        return jsonify({"status": "ACCEPTED", "proposal_id": proposal_id, "value": value})

    return jsonify({"status": "REJECT", "proposal_id": proposal_id})

if __name__ == "__main__":
    print(f"Paxos Node {NODE_ID} starting...")
    app.run(host="0.0.0.0", port=5000)
