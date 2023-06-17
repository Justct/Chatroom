from flask import Flask, request
import requests
import sys

app = Flask(__name__)

room_name = input("The room Name : ")

def P():
    response = requests.get(f"https://backendjustchat.darkmash.repl.co/find/{room_name}")
    return response.text.startswith("http")

@app.route('/verify/if/it/a/chat/room/of/just/chat', methods=['GET'])
def verify_chat_room():
    if P():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return "Flask app stopped"
    else:
        return "Continue running Flask app"
    return room_name




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Please provide the IP and port as command line arguments.")
        print("Usage: python app.py <ip> <port>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=ip, port=port)
