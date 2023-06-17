import subprocess
import os
import platform
import requests
import time
import json


room_name = input("Room Name  : ")
room_url = input("Room URL : ")

f = open("info.json","w")
f.write(json.dumps({"name":room_name, "url" : room_url}))
f.close()


def P():
    response = requests.get(f"https://backendjustchat.darkmash.repl.co/find/{room_name}")
    return response.text == room_url


def start_server(ip, port):
    if not P():
        if platform.system().lower() == "linux":
            os.system(f"python3 verify.py {ip} {port}")
        else:
            os.system(f"python verify.py {ip} {port}")      
    print("WAIT 10 SECS")
    time.sleep(10)
    if not P():
        print("The room url and the url provided didnt match or someother error!! Quiting")
        quit()

    if platform.system().lower() == "linux":
        os.system(f"python3 api.py {ip} {port}")
    else:
        os.system(f"python Chatroom/api.py {ip} {port}")
def start_ngrok(port, use_https):
    print(f"Starting Ngrok on port {port}")
    if use_https:
        subprocess.run(["ngrok", "http", port])
    else:
        subprocess.run(["ngrok", "tcp", port])

def main():
    ip = input("Enter the IP address to run the API (default '0.0.0.0'): ")
    ip = ip.replace(" ", "")
    if ip  == "":
        ip = "0.0.0.0"

    try:
        port =int( input("Enter the port number (default 5010): "))
        port = port.replace(" ", "")
        if port == "":
            port = "5010"
    except:
        port = "5010"

    use_ngrok = input("Do you want to use Ngrok for port forwarding? (y/N): ").lower() == "y"
    if use_ngrok:
        use_https = input("Do you want to use HTTPS or TCP? [using HTTPS provided by ngrok will expose your IP] (y/N): ").lower() == "y"

    if use_ngrok:
        start_ngrok(port, use_https)

    start_server(ip, port)

if __name__ == "__main__":
    main()
