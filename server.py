import socket
import threading

HOST = "0.0.0.0"
PORT = 8000

clients = []
clients_lock = threading.Lock()
def distMsg(message, sender=None):
    with clients_lock:
        deadClients = []
        for client in clients:
            if client != sender:
                try:
                    client.sendall(message)
                except:
                    deadClients.append(client)
        
        for client in deadClients:
            clients.remove(client)

def handleClient(conn, addr):
    with clients_lock:
        clients.append(conn)
    
    print(f"Connected by {addr}")
    distMsg(f"[SERVER]: {addr} joined\n".encode())
    
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"From {addr}: {data.decode()}")
            distMsg(f"{data.decode()}".encode(), conn)
    
    except Exception as e:
        print(f"Error with {addr}: {e}")
    
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()
        print(f"{addr} disconnected")
        distMsg(f"[SERVER]: {addr} left\n".encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()