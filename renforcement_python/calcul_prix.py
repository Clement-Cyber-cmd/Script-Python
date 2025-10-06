def calculer_prix_ttc():
    nom_produit = input("Veuillez entrer le nom du produit : ")
    prix_unitaire = float(input("Veuillez saisir le prix unitaire du produit : "))
    quantité = int(input("Veuillez saisir la quantité : "))
    taux_tva = 20  # TVA en pourcentage

    prix_HT = prix_unitaire * quantité
    montant_TVA = prix_HT * (taux_tva / 100)
    prix_TTC = prix_HT + montant_TVA

    # Affichage formaté avec arrondi à 2 décimales
    print("\n=== FACTURE ===")
    print(f"Produit : {nom_produit}")
    print(f"Quantité : {quantité}")
    print(f"Prix unitaire : {prix_unitaire:.2f} €")
    print(f"Prix HT : {prix_HT:.2f} €")
    print(f"TVA ({taux_tva}%) : {montant_TVA:.2f} €")
    print(f"Prix TTC : {prix_TTC:.2f} €")

# Exemple d'appel de la fonction
calculer_prix_ttc()
