import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# Nom du fichier CSV
FICHIER_CSV = "annuaire.csv"

# Annuaire en mémoire
annuaire = {}

# Charger les contacts depuis le CSV
def charger_annuaire():
    if os.path.exists(FICHIER_CSV):
        with open(FICHIER_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                annuaire[row["Nom"]] = {"numero": row["Téléphone"], "mail": row["Mail"]}

# Sauvegarder les contacts dans le CSV
def sauvegarder_annuaire():
    with open(FICHIER_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Nom", "Téléphone", "Mail"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for nom, infos in annuaire.items():
            writer.writerow({"Nom": nom, "Téléphone": infos["numero"], "Mail": infos["mail"]})

# Fonction pour mettre à jour le tableau avec option de filtre
def afficher_annuaire(filtre=""):
    for row in tree.get_children():
        tree.delete(row)
    for nom, infos in annuaire.items():
        if filtre.lower() in nom.lower() or filtre.lower() in infos['numero'].lower() or filtre.lower() in infos['mail'].lower():
            tree.insert("", tk.END, values=(nom, infos['numero'], infos['mail']))

# Ajouter un contact
def ajouter_contact():
    nom = entry_nom.get()
    numero = entry_numero.get()
    mail = entry_mail.get()
    if not nom or not numero or not mail:
        messagebox.showwarning("Erreur", "Tous les champs doivent être remplis")
        return
    if nom in annuaire:
        messagebox.showwarning("Erreur", f"{nom} existe déjà dans l'annuaire.")
        return
    annuaire[nom] = {"numero": numero, "mail": mail}
    sauvegarder_annuaire()
    afficher_annuaire()
    clear_entries()

# Modifier un contact
def modifier_contact():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Erreur", "Sélectionnez un contact à modifier.")
        return
    item = selected[0]
    ancien_nom = tree.item(item, "values")[0]
    nouveau_nom = entry_nom.get()
    nouveau_numero = entry_numero.get()
    nouveau_mail = entry_mail.get()
    if not nouveau_nom or not nouveau_numero or not nouveau_mail:
        messagebox.showwarning("Erreur", "Tous les champs doivent être remplis")
        return
    if nouveau_nom != ancien_nom and nouveau_nom in annuaire:
        messagebox.showwarning("Erreur", f"{nouveau_nom} existe déjà dans l'annuaire.")
        return
    if nouveau_nom != ancien_nom:
        del annuaire[ancien_nom]
    annuaire[nouveau_nom] = {"numero": nouveau_numero, "mail": nouveau_mail}
    sauvegarder_annuaire()
    afficher_annuaire()
    clear_entries()

# Supprimer un contact
def supprimer_contact():
    selected = tree.selection()
    if selected:
        for item in selected:
            nom = tree.item(item, "values")[0]
            del annuaire[nom]
        sauvegarder_annuaire()
        afficher_annuaire()
        clear_entries()
    else:
        messagebox.showwarning("Erreur", "Sélectionnez un contact à supprimer.")

# Remplir les champs au double-clic
def remplir_champs(event):
    selected = tree.selection()
    if selected:
        item = selected[0]
        nom, numero, mail = tree.item(item, "values")
        entry_nom.delete(0, tk.END)
        entry_nom.insert(0, nom)
        entry_numero.delete(0, tk.END)
        entry_numero.insert(0, numero)
        entry_mail.delete(0, tk.END)
        entry_mail.insert(0, mail)

# Effacer les champs
def clear_entries():
    entry_nom.delete(0, tk.END)
    entry_numero.delete(0, tk.END)
    entry_mail.delete(0, tk.END)

# Tri des colonnes
sort_order = {}
def trier_colonne(col):
    global sort_order
    items = [(tree.set(k, col), k) for k in tree.get_children('')]
    ordre = sort_order.get(col, False)
    items.sort(reverse=ordre)
    for index, (val, k) in enumerate(items):
        tree.move(k, '', index)
    sort_order[col] = not ordre

# Filtre en temps réel
def filtrer(event):
    texte = entry_filtre.get()
    afficher_annuaire(filtre=texte)

# Création fenêtre principale
fenetre = tk.Tk()
fenetre.title("Annuaire CSV")
fenetre.geometry("600x500")

style = ttk.Style(fenetre)
style.theme_use("clam")

# Frame formulaire
frame_form = ttk.Frame(fenetre, padding=10)
frame_form.pack(fill="x")

ttk.Label(frame_form, text="Nom :").grid(row=0, column=0, sticky="w")
entry_nom = ttk.Entry(frame_form, width=30)
entry_nom.grid(row=0, column=1, pady=5)

ttk.Label(frame_form, text="Numéro :").grid(row=1, column=0, sticky="w")
entry_numero = ttk.Entry(frame_form, width=30)
entry_numero.grid(row=1, column=1, pady=5)

ttk.Label(frame_form, text="Mail :").grid(row=2, column=0, sticky="w")
entry_mail = ttk.Entry(frame_form, width=30)
entry_mail.grid(row=2, column=1, pady=5)

# Frame boutons
frame_btns = ttk.Frame(fenetre, padding=10)
frame_btns.pack(fill="x")

ttk.Button(frame_btns, text="Ajouter", command=ajouter_contact).grid(row=0, column=0, padx=5)
ttk.Button(frame_btns, text="Modifier", command=modifier_contact).grid(row=0, column=1, padx=5)
ttk.Button(frame_btns, text="Supprimer", command=supprimer_contact).grid(row=0, column=2, padx=5)

# Filtre
ttk.Label(frame_btns, text="Recherche :").grid(row=0, column=3, padx=5)
entry_filtre = ttk.Entry(frame_btns, width=20)
entry_filtre.grid(row=0, column=4)
entry_filtre.bind("<KeyRelease>", filtrer)

# Frame tableau
frame_table = ttk.Frame(fenetre, padding=10)
frame_table.pack(fill="both", expand=True)

colonnes = ("Nom", "Téléphone", "Mail")
tree = ttk.Treeview(frame_table, columns=colonnes, show="headings", height=15)

for col in colonnes:
    tree.heading(col, text=col, command=lambda _col=col: trier_colonne(_col))
    tree.column(col, width=180)

tree.pack(fill="both", expand=True)
tree.bind("<Double-1>", remplir_champs)

# Charger l'annuaire depuis CSV au démarrage
charger_annuaire()
afficher_annuaire()

# Lancement interface
fenetre.mainloop()

