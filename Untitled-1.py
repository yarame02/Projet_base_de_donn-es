from customtkinter import *
import tkinter as tk
from tkinter import messagebox
import MySQLdb
from PIL import Image, ImageTk

# Fonction pour ajouter un produit
def ajouter_produit():
    nom = champ_nom.get()
    description = champ_description.get()
    prix = champ_prix.get()
    quantite = champ_quantite.get()
    cursor.execute("INSERT INTO gestion_pharmacie_produit (nom, description, prix, quantite_en_stock) VALUES (%s, %s, %s, %s)", 
                   (nom, description, prix, quantite))
    db.commit()
    messagebox.showinfo("Succès", "Produit ajouté avec succès")
    champ_nom.delete(0, tk.END)
    champ_description.delete(0, tk.END)
    champ_prix.delete(0, tk.END)
    champ_quantite.delete(0, tk.END)

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
    canvas.image = image_with_opacity  # Conserver une référence de l'image pour éviter qu'elle soit effacée par le garbage collector
    canvas.create_image(0, 0, image=image_with_opacity, anchor="nw")

# Connexion à la base de données
db = MySQLdb.connect(user='root', password='', host='localhost', database='pharmacie')
cursor = db.cursor()

# Création de l'application avec customtkinter
app = CTk()
app.geometry("1225x700")
app.title("Gestion de la Pharmacie")

tabview = CTkTabview(master=app)
tabview.pack(padx=20, pady=20, fill='both', expand=True)

# Ajouter des onglets
tabview.add("Ajouter des Produits")
tabview.add("Modifier")
tabview.add("Supprimer")
tabview.add("Rechercher")
tabview.add("Tous les produits")
tabview.add("Stock et date de péremption")

# Créer un Canvas pour l'image et les widgets superposés
canvas = tk.Canvas(tabview.tab("Ajouter des Produits"), width=1225, height=700)
canvas.pack(fill="both", expand=True)
canvas1 = tk.Canvas(tabview.tab("Modifier"), width=1225, height=700)
canvas1.pack(fill="both", expand=True)

# Charger et afficher l'image en arrière-plan
image_path = "medoc.jpg"  # Chemin de l'image
image_with_opacity = load_image_with_opacity(image_path, 0.5, (1225, 700))  # Image initiale
canvas.create_image(0, 0, image=image_with_opacity, anchor="nw")  # Ajouter l'image au Canvas
canvas.create_image(0, 0, image=image_with_opacity, anchor="nw")  # Ajouter l'image au Canvas

# Lier l'événement de redimensionnement de la fenêtre pour ajuster l'image
canvas.bind("<Configure>", update_image_size)
canvas.bind("<Configure>", update_image_size)

# Frame pour ajouter un produit
frame = tk.Frame(tabview.tab("Ajouter des Produits"), bg='#e0f7e0', padx=20, pady=20)
frame.pack(fill='both', expand=True)

# Insérer l'image dans le Frame, mais avec un redimensionnement
image_path = "medoc.jpg"  # Remplacez par le chemin de votre image
image_with_opacity = load_image_with_opacity(image_path, 0.5, (200, 200))  # Redimensionner l'image à 200x200 pixels
image_label = tk.Label(frame, image=image_with_opacity, bg='#e0f7e0')
image_label.image = image_with_opacity  # Garder une référence à l'image pour éviter la collecte par le garbage collector
image_label.pack(pady=10)

# Frame pour les champs de saisie
form_frame = tk.Frame(frame, bg='#e0f7e0', padx=20, pady=20)
form_frame.pack(fill='both', expand=True)

# Labels et champs de saisie pour ajouter un produit
tk.Label(form_frame, text="Nom du Produit", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=1, column=0, sticky=tk.E, pady=5)
tk.Label(form_frame, text="Description", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=2, column=0, sticky=tk.E, pady=5)
tk.Label(form_frame, text="Prix", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=3, column=0, sticky=tk.E, pady=5)
tk.Label(form_frame, text="Quantité en Stock", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=4, column=0, sticky=tk.E, pady=5)

# Frame pour modifier un produit
frame1 = tk.Frame(tabview.tab("Modifier"), bg='#e0f7e0', padx=20, pady=20)
frame1.pack(fill='both', expand=True)

# Insérer l'image dans le Frame, mais avec un redimensionnement
image_path1 = "medoc.jpg"  # Remplacez par le chemin de votre image
image_with_opacity1 = load_image_with_opacity(image_path1, 0.5, (200, 200))  # Redimensionner l'image à 200x200 pixels
image_label1 = tk.Label(frame1, image=image_with_opacity1, bg='#e0f7e0')
image_label1.image = image_with_opacity1  # Garder une référence à l'image pour éviter la collecte par le garbage collector
image_label1.pack(pady=10)

# Frame pour les champs de saisie
form_frame1 = tk.Frame(frame1, bg='#e0f7e0', padx=20, pady=20)
form_frame1.pack(fill='both', expand=True)

# Labels et champs de saisie pour ajouter un produit
tk.Label(form_frame1, text="Nom du Produit", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=1, column=0, sticky=tk.E, pady=5)
tk.Label(form_frame1, text="Description", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=2, column=0, sticky=tk.E, pady=5)
tk.Label(form_frame1, text="Prix", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=3, column=0, sticky=tk.E, pady=5)
tk.Label(form_frame1, text="Quantité en Stock", bg='#c8e6c9', font=('Helvetica', 12, 'bold'), padx=10, pady=5).grid(row=4, column=0, sticky=tk.E, pady=5)



# Ajouter des Labels et des Entrées sur l'image
label_font = ('Helvetica', 12, 'bold')
champ_font = ('Helvetica', 12)

canvas.create_text(600, 100, text="Nom du Produit", fill="black", font=label_font)
champ_nom = tk.Entry(app, bg="white", font=champ_font)
canvas.create_window(600, 130, window=champ_nom)

canvas.create_text(600, 180, text="Description", fill="black", font=label_font)
champ_description = tk.Entry(app, bg="white", font=champ_font)
canvas.create_window(600, 210, window=champ_description)

canvas.create_text(600, 260, text="Prix", fill="black", font=label_font)
champ_prix = tk.Entry(app, bg="white", font=champ_font)
canvas.create_window(600, 290, window=champ_prix)

canvas.create_text(600, 340, text="Quantité en Stock", fill="black", font=label_font)
champ_quantite = tk.Entry(app, bg="white", font=champ_font)
canvas.create_window(600, 370, window=champ_quantite)

# Bouton d'ajout de produit
ajouter_btn = tk.Button(app, text='Ajouter Produit', command=ajouter_produit, bg='#81c784', fg='#ffffff', font=label_font)
canvas.create_window(600, 450, window=ajouter_btn)
app.mainloop()
