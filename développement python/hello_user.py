import sys
if len(sys.argv) > 1:
    nom=sys.argv[1]
    print(f"Bonjour, {nom} !")
else:
    print("Usage: python hello_user.py [votre_nom]")