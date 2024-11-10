from customtkinter import *
import tkinter as tk
from tkinter import messagebox
import MySQLdb
from PIL import Image, ImageTk
import customtkinter as ctk

# Fonction pour modifier un produit
def modifier_produit():
    nom = champ_nom1.get()
    description = champ_description1.get()
    prix = champ_prix1.get()
    quantite = champ_quantite1.get()
    cursor.execute("UPDATE gestion_pharmacie_produit SET description=%s, prix=%s, quantite_en_stock=%s WHERE nom=%s", 
                   (description, prix, quantite, nom))
    db.commit()
    messagebox.showinfo("Succès", "Produit modifié avec succès")
    champ_nom1.delete(0, tk.END)
    champ_description1.delete(0, tk.END)
    champ_prix1.delete(0, tk.END)
    champ_quantite1.delete(0, tk.END)

# Charger une image et ajuster sa taille à celle du canvas
def load_image_with_opacity(path, opacity, new_size):
    image = Image.open(path).resize(new_size, Image.Resampling.LANCZOS)
    image = image.convert("RGBA")
    alpha = image.split()[3]
    alpha = alpha.point(lambda p: p * opacity)
    image.putalpha(alpha)
    return ImageTk.PhotoImage(image)

# Redimensionner l'image selon la taille du canvas
def update_image_size(event):
    canvas_width = event.width
    canvas_height = event.height
    image_with_opacity = load_image_with_opacity(image_path, 0.5, (canvas_width, canvas_height))
    event.widget.image = image_with_opacity  # Conserver une référence de l'image pour éviter qu'elle soit effacée par le garbage collector
    event.widget.create_image(0, 0, image=image_with_opacity, anchor="nw")

# Connexion à la base de données
db = MySQLdb.connect(user='root', password='', host='localhost', database='pharmacie')
cursor = db.cursor()

# Création de l'application avec customtkinter
app = CTk()
app.geometry("1225x700")
app.title("Gestion de la Pharmacie")

tabview = CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill='both', expand=True)

tabview.add("Modifier des Produits")
canvas1 = tk.Canvas(tabview.tab("Modifier des Produits"), width=1225, height=700)
canvas1.pack(fill="both", expand=True)

# Charger et afficher l'image en arrière-plan pour les trois onglets
image_path = "medoc.jpg"  # Chemin de l'image
image_with_opacity = load_image_with_opacity(image_path, 0.5, (1225, 700))

canvas1.create_image(0, 0, image=image_with_opacity, anchor="nw") 

canvas1.bind("<Configure>", update_image_size)

# Ajouter des Labels et des Entrées pour l'onglet "Ajouter des Produits"
label_font = ('Helvetica', 12, 'bold')
champ_font = ('Helvetica', 12)

# Ajouter des Labels et des Entrées pour l'onglet "Modifier des Produits"
canvas1.create_text(600, 100, text="Nom du Produit", fill="black", font=label_font)
champ_nom1 = tk.Entry(app, bg="white", font=champ_font)
canvas1.create_window(600, 130, window=champ_nom1)

canvas1.create_text(600, 180, text="Description", fill="black", font=label_font)
champ_description1 = tk.Entry(app, bg="white", font=champ_font)
canvas1.create_window(600, 210, window=champ_description1)

canvas1.create_text(600, 260, text="Prix", fill="black", font=label_font)
champ_prix1 = tk.Entry(app, bg="white", font=champ_font)
canvas1.create_window(600, 290, window=champ_prix1)

canvas1.create_text(600, 340, text="Quantité en Stock", fill="black", font=label_font)
champ_quantite1 = tk.Entry(app, bg="white", font=champ_font)
canvas1.create_window(600, 370, window=champ_quantite1)

# Bouton de modification de produit
modifier_btn = tk.Button(app, text='Modifier Produit', command=modifier_produit, bg='#81c784', fg='#ffffff', font=label_font)
canvas1.create_window(600, 450, window=modifier_btn)

app.mainloop()