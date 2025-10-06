# Création du dictionnaire produit
produit = {
    "nom": "Ordinateur Portable",
    "prix": 1200,
    "stock": 15
}

# Définition de la fonction
def afficher_details_produit(produit):
    print("--- Fiche Produit ---")
    print(f"Nom: {produit['nom']}")
    print(f"Prix: {produit['prix']}")
    print(f"Stock: {produit['stock']} unités")

# Exemple d'utilisation
afficher_details_produit(produit)
