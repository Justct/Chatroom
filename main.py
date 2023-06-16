import subprocess
import os
import platform


def start_server(ip, port):
    if platform.system().lower() == "linux":
        os.system(f"python3 Chatroom/api.py {ip} {port}")
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
