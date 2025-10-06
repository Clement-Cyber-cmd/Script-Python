import os
import zipfile
from datetime import datetime
import argparse

def main():
    parser = argparse.ArgumentParser(description="Archivage des fichiers d'un dossier.")
    parser.add_argument(
        "-s", "--source",
        default="to_process",
        help="Dossier contenant les fichiers à archiver (par défaut: to_process)"
    )
    parser.add_argument(
        "-d", "--dest",
        default="archives",
        help="Dossier où stocker l'archive (par défaut: archives)"
    )
    args = parser.parse_args()

    to_process = args.source
    archives = args.dest

    # Vérifier l'existence du dossier source
    if not os.path.isdir(to_process):
        print(f"Le dossier '{to_process}' n'existe pas.")
        exit(1)

    # Créer le dossier archives s'il n'existe pas
    os.makedirs(archives, exist_ok=True)

    # Nom unique pour l'archive (basé sur date et heure)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"archive_{timestamp}.zip"
    zip_path = os.path.join(archives, zip_name)

    # Création de l’archive
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in os.listdir(to_process):
            chemin_complet = os.path.join(to_process, file)
            if os.path.isfile(chemin_complet):
                archive.write(chemin_complet, file)

    # Vérification : archive bien créée et non vide
    if os.path.exists(zip_path) and os.path.getsize(zip_path) > 0:
        print(f"✅ Archive créée avec succès : {zip_path}")
        
        # Suppression des fichiers originaux
        for file in os.listdir(to_process):
            chemin_complet = os.path.join(to_process, file)
            if os.path.isfile(chemin_complet):
                os.remove(chemin_complet)
                print(f"Supprimé : {chemin_complet}")
    else:
        print("❌ Erreur : l’archivage n’a pas abouti, aucun fichier supprimé.")

if __name__ == "__main__":
    main()


