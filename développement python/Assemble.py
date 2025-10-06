#!/usr/bin/env python3
import json
import os
import datetime
import socket
import subprocess

# ===================== CONFIGURATION =====================
CONFIG = {
    "host": "127.0.0.1",
    "ports": [3389, 80, 443],  # Exemples : RDP, HTTP, HTTPS
    "services": ["Spooler", "wuauserv"],  # Exemples de services Windows
    "log_file": r"C:/Users/cleme/OneDrive/Bureau/System.evtx",  # Exemple de log
    "alert_file": "ALERT.txt",
    "keywords": ["error", "fail", "critical"]
}

# ===================== FONCTIONS =====================

def check_port(host, port):
    """Vérifie si un port est ouvert sur l'hôte donné."""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def check_service_status(service_name):
    """Vérifie si un service Windows est en cours d'exécution via sc query."""
    try:
        result = subprocess.run(
            ["sc", "query", service_name],
            capture_output=True, text=True
        )
        return "RUNNING" in result.stdout
    except Exception:
        return False

def analyze_log(file_path, keywords):
    """Analyse un fichier log texte (Windows Event Logs nécessitent export vers txt)."""
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().lower()
    return any(keyword.lower() in content for keyword in keywords)

# ===================== SCRIPT PRINCIPAL =====================
def main():
    report = {
        "ports": {},
        "services": {},
        "log_analysis": {}
    }

    alert_needed = False

    # Vérification des ports
    for port in CONFIG["ports"]:
        status = check_port(CONFIG["host"], port)
        report["ports"][port] = "OK" if status else "FAIL"
        if not status:
            alert_needed = True

    # Vérification des services
    for service in CONFIG["services"]:
        status = check_service_status(service)
        report["services"][service] = "OK" if status else "FAIL"
        if not status:
            alert_needed = True

    # Analyse des logs
    log_status = analyze_log(CONFIG["log_file"], CONFIG["keywords"])
    report["log_analysis"][CONFIG["log_file"]] = "OK" if not log_status else "FAIL"
    if log_status:
        alert_needed = True

    # Génération d'alerte si nécessaire
    if alert_needed:
        with open(CONFIG["alert_file"], "w") as f:
            f.write(f"ALERTE détectée le {datetime.datetime.now()} !\n")
            f.write("Certaines vérifications ont échoué. Consultez le rapport ci-dessous.\n")

    # Affichage du rapport final en JSON
    print(json.dumps(report, indent=4))

if __name__ == "__main__":
    main()
