from flask import Flask, request
import requests
import sys
import json

app = Flask(__name__)

f = open("info.json", "r")
data_ = json.loads(f.read())
f.close()
room_name = data_["name"]
room_url = data_["url"]

def P():
    response = requests.get(f"https://backendjustchat.darkmash.repl.co/find/{room_name}")
    return response.text == room_url

@app.route('/verify/if/it/a/chat/room/of/just/chat', methods=['GET'])
def verify_chat_room():
    if P():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Flask app stopped"

    return room_name




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Please provide the IP and port as command line arguments.")
        print("Usage: python app.py <ip> <port>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=ip, port=port)
