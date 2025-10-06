# Déclaration des variables
nom = "Clément"       # chaîne de caractères
age = 20              # entier
taille = 1.86         # décimal (float)
etudiant = True       # booléen

# Affichage de chaque variable avec son type
print(f"Variable: {nom}, Type: {type(nom)}")
print(f"Variable: {age}, Type: {type(age)}")
print(f"Variable: {taille}, Type: {type(taille)}")
print(f"Variable: {etudiant}, Type: {type(etudiant)}")

# Calcul et affichage de l'âge dans 10 ans
age_dans_10_ans = age + 10
print(f"Dans 10 ans, j'aurai {age_dans_10_ans} ans.")

# Phrase de présentation utilisant toutes les variables
presentation = f"Je m'appelle {nom}, j'ai {age} ans, je mesure {taille}m et je suis étudiant: {etudiant}"
print(presentation)
