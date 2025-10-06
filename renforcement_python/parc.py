taille = float(input("Entrez votre taille en mètres : "))
age = int(input("Entrez votre âge : "))

if taille > 1.40 and 10 <= age <= 60:
    print("Vous pouvez accéder à l'attraction")
else:
    print("Désolé, vous ne remplissez pas les conditions pour accéder à l'attraction.")