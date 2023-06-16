import sys
import html
import asyncio
import websockets
from datetime import datetime, timedelta



MAX_CONNECTIONS = 1000000  # Maximum allowed concurrent connections
CONNECTION_TIMEOUT = 300  # Connection timeout in seconds
MAX_CONNECTIONS_PER_IP = 3  # Maximum allowed connections per IP address
MAX_MESSAGES_PER_MINUTE = 20  # Maximum allowed messages per minute per IP address



connected = set()
ip_connections = {}
ip_last_message = {}
username_mapping = {}



async def chat(websocket, path):
    # Check maximum concurrent connections
    if len(connected) >= MAX_CONNECTIONS:
        await websocket.close()
        return

    # Check maximum connections per IP
    client_ip = websocket.remote_address[0]
    ip_connections.setdefault(client_ip, 0)
    if ip_connections[client_ip] >= MAX_CONNECTIONS_PER_IP:
        await websocket.close()
        return

    connected.add(websocket)
    ip_connections[client_ip] += 1

    try:
        is_first_message = True
        while True:
            message = await websocket.recv()

            if is_first_message:
                is_first_message = False
                if message in username_mapping.values():
                    await websocket.send("re::re")
                    is_first_message = True
                    continue
                else:
                    username_mapping[websocket] = message
                    await broadcast(f"join::{message}")
            else:
                if not check_rate_limit(client_ip):
                    await websocket.close()
                    return

                await broadcast(f"msg::{username_mapping[websocket]}::{message}")
                update_last_message(client_ip)
    except websockets.exceptions.ConnectionClosed:
        if websocket in username_mapping:
            username = username_mapping.pop(websocket)
            await broadcast(f"left::{username}")

    finally:
        connected.remove(websocket)
        ip_connections[client_ip] -= 1

def check_rate_limit(client_ip):
    # Check if rate limit exceeded
    if client_ip in ip_last_message:
        last_message_time = ip_last_message[client_ip]
        elapsed_time = datetime.now() - last_message_time
        if elapsed_time < timedelta(minutes=1) and ip_connections[client_ip] > MAX_MESSAGES_PER_MINUTE:
            return False
    return True

def update_last_message(client_ip):
    # Update the last message time for the IP address
    ip_last_message[client_ip] = datetime.now()

async def broadcast(message):
    message = html.escape(message)
    for client in connected:
        await client.send(message)

ip = sys.argv[1]
port = sys.argv[2]

start_server = websockets.serve(chat, ip , int(port))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

