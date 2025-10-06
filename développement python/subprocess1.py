import subprocess
command = ['dir', 'C:/Users/cleme/OneDrive/Bureau', '/p']
resultat = subprocess.run(command, capture_output=True, text=True)
if resultat.returncode == 0:
    print("Commande réussie!")
    print("Sortie de la commande :")
    print(resultat.stdout)
else:
    print("la commande à échoué !")
    print("Erreur :")
    print(resultat.stderr)