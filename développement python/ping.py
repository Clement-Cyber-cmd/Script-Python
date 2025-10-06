import socket
def check_port(host, port, timeout=3):
    """Tente de se connecter et retourne True si succès, False sinon."""
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return True
    except socket.error:
        return False
    return False