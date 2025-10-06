def calculer_moyenne(notes):
    # Vérifie si la liste est vide
    if len(notes) == 0:
        return 0  
    
    # Calcule la somme et le nombre d'éléments
    total = sum(notes)
    nombre_elements = len(notes)
    
    # Calcule et renvoie la moyenne
    moyenne = total / nombre_elements
    return moyenne


# Exemple d'utilisation
print(calculer_moyenne([12, 15, 14, 9]))   # ➝ 12.5
print(calculer_moyenne([]))                # ➝ 0
