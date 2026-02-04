
# Host IP addr
HOST: str       = "172.20.42.42"
# Host port
PORT: int       = 8000
# Connection timeout in seconds (how long to wait for a connection before failing)
# Set to None for no timeout
TIMEOUT: float | None  = 3.5

try:
    import socket
    import threading
    import colorama
except:
    print("TermiChat requires pips `socket`, `threading`, and `colorama`")
    answer = input("Try to install packages? [y/N] ").strip().lower()
    if not answer or answer == "n":
        exit(1)
    try:
        import os
    except Exception:
        print("Cannot import the os module")
        exit(1)
    socket_exit = os.system("pip install socket")
    threading_exit = os.system("pip install threading")
    colorama_exit = os.system("pip install colorama")
    if socket_exit != 0 or threading_exit != 0 or colorama_exit != 0:
        print("An error occured while installing the packages")
        if socket_exit != 0:
            exit(socket_exit)
        elif threading_exit != 0:
            exit(threading_exit)
        else:
            exit(colorama_exit)
    try:
        import sys
    except:
        print("cannot import the sys module")
        exit(1)

    sys.stdout.flush()
    sys.stderr.flush()
    x = os.execv(sys.executable, ['python'] + sys.argv)
    exit(x)

socket.setdefaulttimeout(TIMEOUT)

from colorama import Fore
colorama.init(autoreset=True)

def wprint(string: str) -> None:
    print(Fore.YELLOW + string)
def eprint(string: str) -> None:
    print(Fore.RED + string)
def unknown_error(e: Exception) -> None:
    eprint(f"unknown error {e}")

VERSION = "0.1.0"
print("---TERMICHAT---")
print(f"v{VERSION}")
print(f"IP: {HOST}")
print(f"Port: {PORT}")
if TIMEOUT:
    print(f"Timeout: {TIMEOUT}")
else:
    print("No timeout")
wprint("TermiChat is experimental at this time! We are not responsible if anything happens to your system as a result of TermiChat.")
print()

try:
    username = input("Enter your username: ")
    def recvLoop(s: socket.socket):
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(data.decode(), end="")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(Fore.LIGHTGREEN_EX + "Connecting...")
        try:
            s.connect((HOST, PORT))
        except OverflowError:
            eprint("Port invalid, must be between 0-65535")
            exit(1)
        threading.Thread(target=recvLoop, args=(s,), daemon=True).start()
        while True:
            msg = input().strip()
            if msg:
                s.sendall(f"\033[1m[{username}]\033[0m {msg}\n".encode())
            else:
                wprint("Message must have content")
except KeyboardInterrupt:
    wprint("Received ctrl+c, aborting")
except TimeoutError:
    eprint("Timed out, couldn't find server")
    exit(1)
except OSError as e:
    # Match error for invalid socket
    if e.winerror == 10049 or e.errno == 99:
        eprint(f"IP addr {HOST} is invalid")
    else:
        unknown_error(e)
    if e.winerror:
        exit(e.winerror)
    elif e.errno:
        exit(e.errno)
    else:
        exit(1)
except Exception as e:
    unknown_error(e)
    exit(e)