import os
import requests
import json
import platform

room_name = input("Room Name  : ")
room_url = input("Room Domain/Public IP (if ip do ip:8069) : ")

f = open("info.json","w")
f.write(json.dumps({"name":room_name, "url" : room_url}))
f.close()

def P():
    response = requests.get(f"https://justct.pythonanywhere.com/find/{room_name}")
    return response.text == room_url

if P():
    if platform.system().lower() == "windows":
        os.system(f"python app.py 0.0.0.0 8069")
    else:
        os.system(f"python3 api.py 0.0.0.0 8069")


def start_server(ip, port):
    if not P():
        if platform.system().lower() == "windows":
            os.system(f"python verify.py {ip} {port}")
        else:
            os.system(f"python3 verify.py {ip} {port}")      

    if platform.system().lower() == "windows":
        os.system(f"python app.py 0.0.0.0 8069")
    else:
        os.system(f"python3 api.py 0.0.0.0 8069")


def main():
    start_server("0.0.0.0", 8069)
    while True:
        pass
   
if __name__ == "__main__":
    main()
