import socket
import sys
import server as serv
import settings as s

def recv_loop(sock, message_queue):
    """Läuft in separatem Thread, um Nachrichten dauerhaft zu empfangen"""
    while True:
        try:
            data = serv.recv_data(sock)
            if data is None:
                print("[INFO] Verbindung zum Server verloren.")
                break
            message_queue.append(data)
        except Exception as e:
            print(f"[FEHLER] Empfang fehlgeschlagen: {e}")
            break

def connect_to_server(SERVER_IP="127.0.0.1"):
    PORT = 65432
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))

    data = serv.recv_data(sock)
    if data and "error" in data:
        print("[SERVER]:", data["error"])
        sock.close()
        sys.exit()

    s.spieler_id = data["spieler_id"]
    print(f"[INFO] Verbunden als Spieler {s.spieler_id}")
    return sock, s.spieler_id

def get_local_ip():
    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        so.connect(("8.8.8.8", 80))
        ip = so.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        so.close()
    return ip
