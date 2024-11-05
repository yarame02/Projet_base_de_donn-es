from customtkinter import *
import tkinter as tk
from tkinter import messagebox
import MySQLdb
from PIL import Image, ImageTk
import customtkinter as ctk


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

# Fonction pour supprimer un produit
def supprimer_produit():
    nom = champ_nom2.get()
    cursor.execute("DELETE FROM gestion_pharmacie_produit WHERE nom=%s", (nom,))
    db.commit()
    messagebox.showinfo("Succès", "Produit supprimé avec succès")
    champ_nom2.delete(0, tk.END)

# Fonction pour rechercher un produit
def rechercher_produit():
    nom = champ_nom3.get()  # Récupérer le nom du produit depuis le champ de recherche
    cursor.execute("SELECT nom, description, prix, quantite_en_stock FROM gestion_pharmacie_produit WHERE nom=%s", (nom,))
    resultat = cursor.fetchone()  # Récupérer le premier résultat de la requête
    
    if resultat:
        # Si un produit est trouvé, afficher ses détails
        nom, description, prix, quantite_en_stock = resultat
        details = f"Nom: {nom}\nDescription: {description}\nPrix: {prix} FCFA\nQuantité en stock: {quantite_en_stock}"
        messagebox.showinfo("Produit trouvé", details)
    else:
        # Si le produit n'est pas trouvé, afficher une rupture de stock
        messagebox.showwarning("Rupture de stock", "Le produit est en rupture de stock ou n'existe pas.")
    
    champ_nom3.delete(0, tk.END)  # Réinitialiser le champ de recherche


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

# Ajouter des onglets
tabview.add("Ajouter des Produits")
tabview.add("Modifier des Produits")
tabview.add("Supprimer des Produits")
tabview.add("Rechercher")
tabview.add("Tous les produits")
tabview.add("Stock et date de péremption")

# Créer des Canvas pour l'image de fond dans les trois onglets
canvas = tk.Canvas(tabview.tab("Ajouter des Produits"), width=1225, height=700)
canvas.pack(fill="both", expand=True)

canvas1 = tk.Canvas(tabview.tab("Modifier des Produits"), width=1225, height=700)
canvas1.pack(fill="both", expand=True)

canvas2 = tk.Canvas(tabview.tab("Supprimer des Produits"), width=1225, height=700)
canvas2.pack(fill="both", expand=True)

canvas3 = tk.Canvas(tabview.tab("Rechercher"), width=1225, height=700)
canvas3.pack(fill="both", expand=True)

canvas4 = tk.Canvas(tabview.tab("Tous les produits"), width=1225, height=700)
canvas4.pack(fill="both", expand=True)

# Ajouter une scrollbar au canvas de l'onglet "Tous les produits"
scrollbar = tk.Scrollbar(tabview.tab("Tous les produits"), orient="vertical", command=canvas4.yview)
scrollbar.pack(side="right", fill="y")

# Configurer le canvas pour être scrollable
canvas4.configure(yscrollcommand=scrollbar.set)
canvas4.bind("<Configure>", lambda e: canvas4.configure(scrollregion=canvas4.bbox("all")))


canvas5 = tk.Canvas(tabview.tab("Stock et date de péremption"), width=1225, height=700)
canvas5.pack(fill="both", expand=True)

# Charger et afficher l'image en arrière-plan pour les trois onglets
image_path = "medoc.jpg"  # Chemin de l'image
image_with_opacity = load_image_with_opacity(image_path, 0.5, (1225, 700))

canvas.create_image(0, 0, image=image_with_opacity, anchor="nw")  
canvas1.create_image(0, 0, image=image_with_opacity, anchor="nw")
canvas2.create_image(0, 0, image=image_with_opacity, anchor="nw")
canvas3.create_image(0, 0, image=image_with_opacity, anchor="nw")
canvas4.create_image(0, 0, image=image_with_opacity, anchor="nw")
canvas5.create_image(0, 0, image=image_with_opacity, anchor="nw")

# Lier l'événement de redimensionnement de la fenêtre pour ajuster l'image
canvas.bind("<Configure>", update_image_size)
canvas1.bind("<Configure>", update_image_size)
canvas2.bind("<Configure>", update_image_size)
canvas3.bind("<Configure>", update_image_size)
canvas4.bind("<Configure>", update_image_size)
canvas5.bind("<Configure>", update_image_size)

# Ajouter des Labels et des Entrées pour l'onglet "Ajouter des Produits"
label_font = ('Helvetica', 12, 'bold')
champ_font = ('Helvetica', 12)

canvas.create_text(200, 100, text="Nom du Produit", fill="black", font=label_font)
champ_nom = tk.Entry(app, bg="white", font=champ_font)
canvas.create_window(600, 100, window=champ_nom)

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

# Ajouter des Labels et des Entrées pour l'onglet "Supprimer des Produits"
canvas2.create_text(600, 100, text="Nom du Produit", fill="black", font=label_font)
champ_nom2 = tk.Entry(app, bg="white", font=champ_font)
canvas2.create_window(600, 130, window=champ_nom2)

# Bouton de suppression de produit
supprimer_btn = tk.Button(app, text='Supprimer Produit', command=supprimer_produit, bg='#81c784', fg='#ffffff', font=label_font)
canvas2.create_window(600, 450, window=supprimer_btn)

# Ajouter des Labels et des Entrées pour l'onglet "Rechercher des Produits"
canvas3.create_text(600, 100, text="Nom du Produit", fill="black", font=label_font)
champ_nom3 = tk.Entry(app, bg="white", font=champ_font)
canvas3.create_window(600, 130, window=champ_nom3)

# Bouton de recherche de produit
rechercher_btn = tk.Button(app, text='Rechercher Produit', command=rechercher_produit, bg='#81c784', fg='#ffffff', font=label_font)
canvas3.create_window(600, 450, window=rechercher_btn)


# Fonction pour afficher tous les produits (mise à jour)
def afficher_tous_les_produits():
    # Vider le canvas avant d'ajouter les nouveaux produits
    canvas4.delete("all")
    
    # Charger l'image de fond avec l'opacité
    image_with_opacity = load_image_with_opacity(image_path, 0.5, (1225, 700))
    canvas4.create_image(0, 0, image=image_with_opacity, anchor="nw")
    
    # Récupérer les produits de la base de données
    cursor.execute("SELECT nom, description, prix, quantite_en_stock FROM gestion_pharmacie_produit")
    produits = cursor.fetchall()
    
    if produits:
        y_position = 100  # Position initiale Y
        padding_x = 50  # Espace à gauche
        box_width = 1100  # Largeur du cadre
        box_height = 120  # Hauteur de chaque cadre produit
        text_color = "#2C3E50"  # Couleur du texte
        box_color = "#ECF0F1"  # Couleur de fond des cadres
        border_color = "#2980B9"  # Couleur des bordures
        
        for produit in produits:
            nom, description, prix, quantite_en_stock = produit
            details_nom = f"Nom: {nom}"
            details_description = f"Description: {description}"
            details_prix = f"Prix: {prix} FCFA"
            details_quantite = f"Quantité: {quantite_en_stock}"

            # Créer un cadre autour de chaque produit
            canvas4.create_rectangle(padding_x, y_position, padding_x + box_width, y_position + box_height, outline=border_color, width=2, fill=box_color)

            # Afficher les informations du produit dans le cadre
            canvas4.create_text(padding_x + 20, y_position + 20, anchor="nw", text=details_nom, fill=text_color)
            canvas4.create_text(padding_x + 20, y_position + 50, anchor="nw", text=details_description, fill=text_color)
            canvas4.create_text(padding_x + 20, y_position + 80, anchor="nw", text=details_prix, fill=text_color)
            canvas4.create_text(padding_x + 500, y_position + 80, anchor="nw", text=details_quantite, fill=text_color)
            
            y_position += box_height + 20  # Espacement entre chaque produit

    # Mettre à jour la région scrollable du canvas
    canvas4.configure(scrollregion=canvas4.bbox("all"))

# Appeler la fonction pour afficher les produits
afficher_tous_les_produits()

# Fonction pour afficher tous les produits avec quantité <= 1
def afficher_stock_et_date_de_peremption():
    # Vider le canvas avant d'ajouter les nouveaux produits
    canvas5.delete("all")

    # Charger l'image de fond avec l'opacité
    image_with_opacity = load_image_with_opacity(image_path, 0.5, (1225, 700))
    canvas5.create_image(0, 0, image=image_with_opacity, anchor="nw")

    # Récupérer les produits de la base de données avec une quantité <= 1
    cursor.execute("SELECT nom FROM gestion_pharmacie_produit WHERE quantite_en_stock <= 1")
    produits = cursor.fetchall()

    if produits:
        y_position = 100  # Position initiale Y
        padding_x = 50  # Espace à gauche
        frame_height = 50  # Hauteur de chaque cadre

        for produit in produits:
            nom = produit
            
            # Créer un cadre pour chaque produit
            frame = ctk.CTkFrame(canvas5, width=1100, height=frame_height, corner_radius=10)
            frame.place(x=padding_x, y=y_position)

            # Créer des éléments de texte pour le produit
            details_nom = f"Nom: {nom}"

            # Afficher le nom du produit
            label_nom = ctk.CTkLabel(frame, text=details_nom, text_color="black", font=("Arial", 14, "bold"))
            label_nom.pack(side="top", anchor="w", padx=10, pady=5)

            y_position += frame_height + 10  # Espacer les produits
    else:
        # Afficher un message si aucun produit n'est en rupture de stock
        canvas5.create_text(600, 100, text="Aucun produit en rupture de stock.", fill="black", font=("Arial", 16, "italic"), anchor="center")

# Appeler cette fonction au démarrage de l'application pour afficher les produits directement
afficher_stock_et_date_de_peremption()
# Charger l'application principale
app.mainloop()
