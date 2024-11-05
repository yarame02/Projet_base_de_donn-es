import tkinter as tk
from tkinter import messagebox
import MySQLdb

# Connexion à la base de données
db = MySQLdb.connect(user='root', password='', host='localhost', database='pharmacie')
cursor = db.cursor()

# Fonction pour ajouter un produit
def ajouter_produit():
    nom = entry_nom.get()
    description = entry_description.get()
    prix = entry_prix.get()
    quantite = entry_quantite.get()
    cursor.execute("INSERT INTO gestion_pharmacie_produit (nom, description, prix, quantite_en_stock) VALUES (%s, %s, %s, %s)", 
                   (nom, description, prix, quantite))
    db.commit()
    messagebox.showinfo("Succès", "Produit ajouté avec succès")
    entry_nom.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_prix.delete(0, tk.END)
    entry_quantite.delete(0, tk.END)

# Interface Tkinter
root = tk.Tk()
root.title("Gestion des Produits")

# Configurer la couleur de fond
root.configure(bg='#e0f7e0')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False, False)
# Créer un cadre pour centrer les éléments
frame = tk.Frame(root, bg='#e0f7e0', padx=20, pady=20)
frame.pack(expand=True)

# Couleurs
label_bg = '#c8e6c9'
entry_bg = '#a5d6a7'
button_bg = '#81c784'
button_fg = '#ffffff'

# Police
label_font = ('Helvetica', 12, 'bold')
entry_font = ('Helvetica', 12)
button_font = ('Helvetica', 12, 'bold')

# Labels
tk.Label(frame, text="Nom du Produit", bg=label_bg, font=label_font, padx=10, pady=5).grid(row=0, column=0, sticky=tk.E, pady=5)
tk.Label(frame, text="Description", bg=label_bg, font=label_font, padx=10, pady=5).grid(row=1, column=0, sticky=tk.E, pady=5)
tk.Label(frame, text="Prix", bg=label_bg, font=label_font, padx=10, pady=5).grid(row=2, column=0, sticky=tk.E, pady=5)
tk.Label(frame, text="Quantité en Stock", bg=label_bg, font=label_font, padx=10, pady=5).grid(row=3, column=0, sticky=tk.E, pady=5)

# Entrées
entry_nom = tk.Entry(frame, bg=entry_bg, font=entry_font, borderwidth=2, relief='solid')
entry_description = tk.Entry(frame, bg=entry_bg, font=entry_font, borderwidth=2, relief='solid')
entry_prix = tk.Entry(frame, bg=entry_bg, font=entry_font, borderwidth=2, relief='solid')
entry_quantite = tk.Entry(frame, bg=entry_bg, font=entry_font, borderwidth=2, relief='solid')

entry_nom.grid(row=0, column=1, pady=5, padx=5, sticky='ew')
entry_description.grid(row=1, column=1, pady=5, padx=5, sticky='ew')
entry_prix.grid(row=2, column=1, pady=5, padx=5, sticky='ew')
entry_quantite.grid(row=3, column=1, pady=5, padx=5, sticky='ew')

# Bouton
tk.Button(frame, text='Ajouter Produit', command=ajouter_produit, bg=button_bg, fg=button_fg, font=button_font, padx=10, pady=5).grid(row=4, columnspan=2, pady=20)

# Centrer les éléments
for i in range(4):
    frame.grid_rowconfigure(i, weight=1)
frame.grid_columnconfigure(1, weight=1)

root.mainloop()
