import subprocess
import logging
import os
import json
import requests
import time
import shutil

# === CONFIG LOGGING ===
logging.basicConfig(
    filename="deploy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SERVICE_NAME = "Spooler"
NGINX_DIR = r"C:\nginx"
NGINX_EXE = os.path.join(NGINX_DIR, "nginx.exe")
HTML_PATH = os.path.join(NGINX_DIR, "html", "index.html")
CONF_PATH = os.path.join(NGINX_DIR, "conf", "nginx.conf")
VHOST_NAME = "nexa.local"

REPORT = {
    "spooler_installed": False,
    "spooler_running": False,
    "nginx_installed": False,
    "nginx_started": False,
    "vhost_created": False,
    "html_created": False,
    "http_check": False,
    "notification": False
}


def run_cmd(cmd):
    """Exécuter une commande et renvoyer stdout."""
    try:
        result = subprocess.run(
            cmd, shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur commande: {cmd} - {e}")
        return None


# === PARTIE SPOOLER ===
def check_spooler():
    """Vérifie si le service Spooler existe."""
    output = run_cmd(f'sc query "{SERVICE_NAME}"')
    if output and "STATE" in output:
        REPORT["spooler_installed"] = True
        logging.info("Service Spooler trouvé")
    else:
        logging.error("Service Spooler introuvable (installation manuelle requise)")


def start_spooler():
    """Démarre le service Spooler si nécessaire."""
    if not REPORT["spooler_installed"]:
        return
    status = run_cmd(f'sc query "{SERVICE_NAME}"')
    if status and "RUNNING" in status:
        logging.info("Spooler déjà en cours d'exécution")
        REPORT["spooler_running"] = True
    else:
        run_cmd(f'sc start "{SERVICE_NAME}"')
        time.sleep(2)
        status = run_cmd(f'sc query "{SERVICE_NAME}"')
        if status and "RUNNING" in status:
            REPORT["spooler_running"] = True
            logging.info("Spooler démarré avec succès")
        else:
            logging.error("Impossible de démarrer Spooler")


# === PARTIE NGINX / VHOST ===
def check_nginx():
    """Vérifie si Nginx est installé."""
    if os.path.exists(NGINX_EXE):
        REPORT["nginx_installed"] = True
        logging.info("Nginx déjà installé")
        return True
    else:
        logging.info("Nginx non trouvé")
        return False


def install_nginx():
    """Télécharge et installe Nginx sous Windows."""
    logging.info("Installation de Nginx...")
    url = "https://nginx.org/download/nginx-1.26.2.zip"
    zip_file = "nginx.zip"
    try:
        r = requests.get(url, stream=True)
        with open(zip_file, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        shutil.unpack_archive(zip_file, NGINX_DIR)
        os.remove(zip_file)
        REPORT["nginx_installed"] = True
        logging.info("Nginx installé avec succès")
    except Exception as e:
        logging.error(f"Erreur installation Nginx: {e}")


def start_nginx():
    """Démarre Nginx."""
    if not REPORT["nginx_installed"]:
        return
    logging.info("Démarrage de Nginx...")
    run_cmd(f'start "" "{NGINX_EXE}"')
    time.sleep(2)
    REPORT["nginx_started"] = True


def create_vhost():
    """Créer un virtual host nexa.local avec Hello Nexa."""
    try:
        # Créer HTML
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write("<html><head><title>Hello Nexa</title></head><body><h1>Hello Nexa</h1></body></html>")
        REPORT["html_created"] = True
        logging.info("Page HTML créée")

        # Configurer vhost dans nginx.conf
        server_block = f"""
worker_processes  1;
events {{
    worker_connections  1024;
}}
http {{
    include       mime.types;
    default_type  application/octet-stream;

    server {{
        listen       80;
        server_name  {VHOST_NAME};
        root         {NGINX_DIR}\\html;
        index        index.html;
    }}
}}
"""
        with open(CONF_PATH, "w", encoding="utf-8") as f:
            f.write(server_block)

        REPORT["vhost_created"] = True
        logging.info("Virtual host créé")
        run_cmd(f'"{NGINX_EXE}" -s reload')
    except Exception as e:
        logging.error(f"Erreur création vhost: {e}")


def check_http():
    """Vérifie la réponse HTTP 200 sur nexa.local."""
    try:
        response = requests.get(f"http://{VHOST_NAME}", timeout=5)
        if response.status_code == 200:
            REPORT["http_check"] = True
            logging.info("Page répond avec 200")
    except Exception as e:
        logging.error(f"Erreur HTTP: {e}")


# === NOTIFICATION ===
def send_notification():
    """Envoie une notification via ntfy."""
    try:
        status = "✅ Déploiement réussi" if all(REPORT.values()) else "❌ Problème lors du déploiement"
        run_cmd(f'curl -s -d "{status}" ntfy.sh/nexa-deploy')
        REPORT["notification"] = True
        logging.info("Notification envoyée")
    except Exception as e:
        logging.error(f"Erreur notification: {e}")


# === MAIN ===
if __name__ == "__main__":
    logging.info("=== Début du déploiement Windows (Spooler + Nginx) ===")

    # Spooler
    check_spooler()
    start_spooler()

    # Nginx + vhost
    if not check_nginx():
        install_nginx()
    start_nginx()
    create_vhost()
    check_http()

    # Notification
    send_notification()

    logging.info("=== Fin du déploiement ===")
    print(json.dumps(REPORT, indent=4))



