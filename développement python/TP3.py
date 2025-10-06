import sys

def compter_occurrences(fichier, mot_cle):
    """Compte les lignes contenant mot_cle dans fichier."""
    count = 0
    try:
        with open(fichier, "r") as f:
            for line in f:
                if mot_cle in line:
                    count += 1
        return count
    except FileNotFoundError:
        print(f"Erreur : le fichier '{fichier}' est introuvable.")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python TP3.py <fichier_log> <mot_cle>")
        sys.exit(1)

    fichier = sys.argv[1]
    mot_cle = sys.argv[2].upper()   # ex: ERROR, WARN, CRITICAL, INFO, DEBUG

    nb = compter_occurrences(fichier, mot_cle)
    if nb is not None:
        print(f"Nombre de lignes contenant '{mot_cle}' : {nb}")



