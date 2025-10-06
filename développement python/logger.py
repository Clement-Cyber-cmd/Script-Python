import logging
import datetime

# Configuration du journal
logging.basicConfig(
    filename='evenements.log',      # Nom du fichier de log
    level=logging.DEBUG,             # Niveau minimal à journaliser
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format des messages
    datefmt='%Y-%m-%d %H:%M:%S'     # Format de la date
)

def log_evenements():
    logging.debug("Ceci est un message de débogage.")        # Debug
    logging.info("Ceci est un message d'information.")       # Information
    logging.warning("Ceci est un avertissement.")            # Avertissement
    logging.error("Ceci est un message d'erreur.")           # Erreur
    logging.critical("Ceci est un message critique.")        # Critique

if __name__ == "__main__":
    logging.info("Le script de journalisation a démarré.")
    log_evenements()
    logging.info("Le script de journalisation s'est terminé.")
