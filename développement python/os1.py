import os

dossier = "C:/Users/cleme/OneDrive/Bureau"
if os.path.exists(dossier):
    print(f"Contenu du dossier (dossier) :")
    contenu = os.listdir(dossier)
    print(contenu[:5])
else:
    print(f"le dossier (dossier) n'existe pas")