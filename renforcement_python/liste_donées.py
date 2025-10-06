Liste = [15, 1, 3, 122, 5, 8, 143]

plus_grand = Liste[0]  
# Parcours de la liste avec une boucle for
for nombre in Liste:
    # Vérification pair/impair
    if nombre % 2 == 0:
        print(f"{nombre} est pair")
    else:
        print(f"{nombre} est impair")
    
    # Vérification du plus grand nombre
    if nombre > plus_grand:
        plus_grand = nombre
        print(f"--> Nouveau plus grand trouvé : {plus_grand}")

# Affichage final
print(f"Le plus grand nombre de la liste est : {plus_grand}")
