from customtkinter import *
import tkinter as tk
from tkinter import messagebox
import MySQLdb

# Fonction pour modifier un produit
def modifier_produit(nom):
    def save_changes():
        new_nom = champ_nom_modif.get()
        new_description = champ_description_modif.get()
        new_prix = champ_prix_modif.get()
        new_quantite = champ_quantite_modif.get()
        new_date = champ_date_modif.get()

        if not new_nom or not new_description or not new_prix or not new_quantite or not new_date:
            messagebox.showwarning("Champs vides", "Tous les champs doivent être remplis.")
            return

        try:
            cursor.execute("UPDATE gestion_pharmacie_produit SET nom=%s, description=%s, prix=%s, quantite_en_stock=%s, date_peremption=%s WHERE nom=%s",
                           (new_nom, new_description, new_prix, new_quantite, new_date, nom))
            db.commit()
            messagebox.showinfo("Succès", "Produit modifié avec succès")
            window_modif.destroy()
        except MySQLdb.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification du produit: {e}")
            db.rollback()

    window_modif = CTkToplevel(app)
    window_modif.title(f"Modifier {nom}")
    window_modif.geometry("600x400")
    window_modif.configure(bg="#f7f7f7")

    # Récupération des informations actuelles
    cursor.execute("SELECT nom, description, prix, quantite_en_stock, date_peremption FROM gestion_pharmacie_produit WHERE nom=%s", (nom,))
    produit = cursor.fetchone()

    if produit:
        nom_actuel, description_actuelle, prix_actuel, quantite_actuelle, date_peremption_actuelle = produit

        # Labels et Champs
        champ_nom_modif = CTkEntry(window_modif, width=250, font=('Helvetica', 14))
        champ_nom_modif.insert(0, nom_actuel)
        champ_description_modif = CTkEntry(window_modif, width=250, font=('Helvetica', 14))
        champ_description_modif.insert(0, description_actuelle)
        champ_prix_modif = CTkEntry(window_modif, width=250, font=('Helvetica', 14))
        champ_prix_modif.insert(0, prix_actuel)
        champ_quantite_modif = CTkEntry(window_modif, width=250, font=('Helvetica', 14))
        champ_quantite_modif.insert(0, quantite_actuelle)
        champ_date_modif = CTkEntry(window_modif, width=250, font=('Helvetica', 14))
        champ_date_modif.insert(0, date_peremption_actuelle)

        # Disposition
        form_data = [
            ("Nom du Produit", champ_nom_modif),
            ("Description", champ_description_modif),
            ("Prix (FCFA)", champ_prix_modif),
            ("Quantité en Stock", champ_quantite_modif),
            ("Date de Péremption", champ_date_modif)
        ]

        for i, (label_text, entry) in enumerate(form_data):
            CTkLabel(window_modif, text=label_text, font=('Helvetica', 14)).grid(row=i, column=0, padx=20, pady=5, sticky="e")
            entry.grid(row=i, column=1, padx=20, pady=5)

        btn_save = CTkButton(window_modif, text="Sauvegarder", font=('Helvetica', 16), command=save_changes,
                             fg_color="#4CAF50", hover_color="#388E3C")
        btn_save.grid(row=len(form_data), column=0, columnspan=2, pady=20)
    else:
        messagebox.showerror("Erreur", "Produit introuvable.")

# Connexion à la base de données
db = MySQLdb.connect(user='root', password='', host='localhost', database='pharmacie')
cursor = db.cursor()

# Création de l'application principale
app = CTk()
app.geometry("800x600")
app.title("Gestion de la Pharmacie")
app.configure(bg="#f5f5f5")

# Interface avec CTkTabview
tabview = CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill='both', expand=True)
tabview.add("Modifier des Produits")

# Champ de recherche
CTkLabel(tabview.tab("Modifier des Produits"), text="Nom du Produit à Modifier", font=('Helvetica', 14)).pack(pady=10)
champ_nom_recherche = CTkEntry(tabview.tab("Modifier des Produits"), font=('Helvetica', 14), width=250)
champ_nom_recherche.pack(pady=5)

# Bouton de recherche et modification
def recherche_produit():
    nom = champ_nom_recherche.get()
    if nom:
        modifier_produit(nom)
    else:
        messagebox.showwarning("Champ Vide", "Veuillez entrer le nom du produit.")

modifier_btn = CTkButton(tabview.tab("Modifier des Produits"), text="Rechercher et Modifier", command=recherche_produit,
                         font=('Helvetica', 14), fg_color='#2196F3', hover_color="#1976D2")
modifier_btn.pack(pady=20)

app.mainloop()