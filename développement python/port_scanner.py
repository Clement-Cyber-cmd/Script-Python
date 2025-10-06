import socket
import argparse

def check_port(host, port, timeout=1):
    """Vérifie si un port est ouvert sur un hôte donné"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except (socket.timeout, socket.error):
            return False

def main():
    parser = argparse.ArgumentParser(description="Outil de scan de ports")
    parser.add_argument("--host", required=True, help="Adresse IP ou nom d'hôte à scanner")
    parser.add_argument("--ports", required=True, help="Liste des ports séparés par des virgules (ex: 22,80,443)")

    args = parser.parse_args()

    host = args.host
    ports = [int(p.strip()) for p in args.ports.split(",")]

    print(f"Scan de {host} sur les ports : {ports}\n")

    for port in ports:
        if check_port(host, port):
            print(f"Port {port} : OUVERT")
        else:
            print(f"Port {port} : FERMÉ")

if __name__ == "__main__":
    main()
