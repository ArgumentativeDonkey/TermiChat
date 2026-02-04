import socket
import threading

HOST = "172.20.42.42"
PORT = 8000
print("connecting...")
username = input("Enter your username: ")
def recvLoop(s):
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(data.decode(), end="")
print("scanning for server...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    threading.Thread(target=recvLoop, args=(s,), daemon=True).start()
    while True:
        msg = input()
        s.sendall(f"\033[1m[{username}]\033[0m {msg}\n".encode())