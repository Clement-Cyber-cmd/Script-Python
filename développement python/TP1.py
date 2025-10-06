import sys

# Vérifier qu'un argument a été donné
if len(sys.argv) < 2:
    print("Usage : python TP1.py <nombre_a_deviner>")
    sys.exit(1)

try:
    a = int(sys.argv[1])  # Le nombre à deviner est passé en paramètre
except ValueError:
    print("Erreur : l'argument doit être un entier.")
    sys.exit(1)

proposition = None

while proposition != a:
    try:
        proposition = int(input("Choisis un nombre : "))
        if proposition > a:
            print("C'est moins")
        elif proposition < a:
            print("C'est plus")
        else:
            print("C'est gagné !")
            sys.exit(0)
    except ValueError:
        print("Erreur : tu dois entrer un nombre entier.")
    except KeyboardInterrupt:
        print("\nPartie interrompue.")
        sys.exit(1)

