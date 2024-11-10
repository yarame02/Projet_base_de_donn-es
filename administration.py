from customtkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import MySQLdb
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Database connection
db = MySQLdb.connect(user='root', password='', host='localhost', database='pharmacie')
cursor = db.cursor()

# Functions
def ajouter_produit():
    # Récupérer les valeurs des champs
    nom = champ_nom.get()
    description = champ_description.get()
    prix = champ_prix.get()
    quantite = champ_quantite.get()
    date_peremption = champ_date.get()  # Récupère la date saisie

    # Vérifier si un des champs est vide
    if not nom or not description or not prix or not quantite or not date_peremption:
        messagebox.showwarning("Champs vides", "Tous les champs doivent être remplis.")
        return  # Ne pas exécuter la suite de la fonction si les champs sont vides

    # Si tous les champs sont remplis, ajouter le produit à la base de données
    try:
        cursor.execute("INSERT INTO gestion_pharmacie_produit (nom, description, prix, quantite_en_stock, date_peremption) VALUES (%s, %s, %s, %s, %s)", 
                       (nom, description, prix, quantite, date_peremption))
        db.commit()
        messagebox.showinfo("Succès", "Produit ajouté avec succès")
    except MySQLdb.Error as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit: {e}")
        db.rollback()

    # Effacer les champs après l'ajout du produit
    champ_nom.delete(0, tk.END)
    champ_description.delete(0, tk.END)
    champ_prix.delete(0, tk.END)
    champ_quantite.delete(0, tk.END)
    champ_date.delete(0, tk.END)

# Fonction qui appelle la modification via le module `modif`
def modifier_produit(nom):
    # Appelle la fonction de modification dans le module `modif`
    from modif import modifier_produit
    modifier_produit()


def supprimer_produit(nom):
    cursor.execute("DELETE FROM gestion_pharmacie_produit WHERE nom=%s", (nom,))
    db.commit()
    messagebox.showinfo("Succès", "Produit supprimé avec succès")
    afficher_tous_les_produits()

def afficher_tous_les_produits():
    canvas4.delete("all")
    canvas4.create_image(0, 0, image=image_with_opacity, anchor="nw")
    cursor.execute("SELECT nom, description, prix, quantite_en_stock, date_peremption FROM gestion_pharmacie_produit")
    produits = cursor.fetchall()
    
    y_position = 50
    for produit in produits:
        nom, description, prix, quantite_en_stock, date_peremption = produit
        cadre_produit = CTkFrame(tabview.tab("Tous les produits"), fg_color="white", corner_radius=10, border_width=1)
        cadre_produit_window = canvas4.create_window(400, y_position, anchor="nw", window=cadre_produit, width=1400, height=40)

        CTkLabel(cadre_produit, text=f"Nom: {nom}", text_color="black", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
        CTkLabel(cadre_produit, text=f"Description: {description}", text_color="black", font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=5)
        CTkLabel(cadre_produit, text=f"Prix: {prix} FCFA", text_color="black", font=("Arial", 14)).grid(row=0, column=2, padx=10, pady=5)
        CTkLabel(cadre_produit, text=f"Quantité: {quantite_en_stock}", text_color="black", font=("Arial", 14)).grid(row=0, column=3, padx=10, pady=5)
        CTkLabel(cadre_produit, text=f"Date de peremption: {date_peremption}", text_color="black", font=("Arial", 14)).grid(row=0, column=4, padx=10, pady=5)

        CTkButton(cadre_produit, text="Modifier", fg_color="blue", width=80, command=lambda n=nom: modifier_produit(n)).grid(row=0, column=5, padx=10)



        CTkButton(cadre_produit, text="Supprimer", fg_color="red", width=80, command=lambda n=nom: supprimer_produit(n)).grid(row=0, column=6, padx=10)
        
        y_position += 70
        # Refresh every 1000ms (1 second)
    canvas4.after(5000, afficher_tous_les_produits)


# App setup
app = CTk()
app_width = 1600
app_height = 800
app.geometry(f"{app_width}x{app_height}")
# Récupérer les dimensions de l'écran
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculer la position centrée
x = (screen_width // 2) - (app_width // 2)
y = (screen_height // 2) - (app_height // 2)

# Positionner la fenêtre au centre
app.geometry(f"{app_width}x{app_height}+{x}+{y}")
app.title("Gestion de la Pharmacie")
app.configure(bg="#EDEDED")

# Tabs configuration
tabview = CTkTabview(app, width=1200, height=650, segmented_button_selected_color="green")
tabview.pack(padx=20, pady=20, fill='both', expand=True)
tabview.add("Ajouter un produit")
tabview.add("Tous les produits")
tabview.add("Rupture de stock")

# Background Image
def load_image_with_opacity(path, opacity, new_size):
    image = Image.open(path).resize(new_size, Image.Resampling.LANCZOS)
    image = image.convert("RGBA")
    alpha = image.split()[3]
    alpha = alpha.point(lambda p: p * opacity)
    image.putalpha(alpha)
    return ImageTk.PhotoImage(image)

image_path = "medoc.jpg"
image_with_opacity = load_image_with_opacity(image_path, 0.5, (1850, 900))

def update_background_image(event=None):
    global image_with_opacity
    window_width = app.winfo_width()
    window_height = app.winfo_height()
    image_with_opacity = load_image_with_opacity(image_path, 0.5, window_width, window_height)


# Canvas for "Add Product" tab
canvas1 = tk.Canvas(tabview.tab("Ajouter un produit"), width=1225, height=650, bg="#EDEDED", bd=0, highlightthickness=0)
canvas1.pack(fill="both", expand=True)
canvas1.create_image(0, 0, image=image_with_opacity, anchor="nw")

# Canvas for "All Products" tab with scrollbar
canvas4 = tk.Canvas(tabview.tab("Tous les produits"), width=1225, height=650, bg="#EDEDED", bd=0, highlightthickness=0)
canvas4.pack(fill="both", expand=True)
scrollbar = tk.Scrollbar(tabview.tab("Tous les produits"), orient="vertical", command=canvas4.yview)
scrollbar.pack(side="right", fill="y")
canvas4.configure(yscrollcommand=scrollbar.set)
canvas4.create_image(0, 0, image=image_with_opacity, anchor="nw")
canvas4.bind("<Configure>", lambda e: canvas4.configure(scrollregion=canvas4.bbox("all")))

# Canvas for "Stock and Expiration Date" tab
canvas2 = tk.Canvas(tabview.tab("Rupture de stock"), width=1225, height=650, bg="#EDEDED", bd=0, highlightthickness=0)
canvas2.pack(fill="both", expand=True)
canvas2.create_image(0, 0, image=image_with_opacity, anchor="nw")

# Form labels and fields with customized design
label_font = ('Helvetica', 18, 'bold')
champ_font = ('Helvetica', 16)
canvas1.create_text(650, 190, text="Nom du Produit", fill="black", font=label_font)
champ_nom = tk.Entry(app, font=champ_font, width=30, bg="white", relief="solid", bd=1)
canvas1.create_window(1100, 190, window=champ_nom)

canvas1.create_text(650, 260, text="Description", fill="black", font=label_font)
champ_description = tk.Entry(app, font=champ_font, width=30, bg="white", relief="solid", bd=1)
canvas1.create_window(1100, 260, window=champ_description)

canvas1.create_text(650, 330, text="Prix (FCFA)", fill="black", font=label_font)
champ_prix = tk.Entry(app, font=champ_font, width=30, bg="white", relief="solid", bd=1)
canvas1.create_window(1100, 330, window=champ_prix)

canvas1.create_text(650, 400, text="Quantité en Stock", fill="black", font=label_font)
champ_quantite = tk.Entry(app, font=champ_font, width=30, bg="white", relief="solid", bd=1)
canvas1.create_window(1100, 400, window=champ_quantite)

canvas1.create_text(650, 470, text="Date de peremption", fill="black", font=label_font)
champ_date = tk.Entry(app, font=champ_font, width=30, bg="white", relief="solid", bd=1)
canvas1.create_window(1100, 470, window=champ_date)

# Submit Button with custom design
btn_ajouter = CTkButton(app, text="Ajouter le Produit", font=('Helvetica', 25, 'bold'), fg_color="#4CAF50", text_color="white", width=20, corner_radius=20, command=ajouter_produit)
canvas1.create_window(950, 750, window=btn_ajouter)

def afficher_stock_et_date_de_peremption():
    canvas2.delete("all")
    canvas2.create_image(0, 0, image=image_with_opacity, anchor="nw")

    cursor.execute("SELECT nom, quantite_en_stock, date_peremption FROM gestion_pharmacie_produit WHERE quantite_en_stock <= 10")
    produits = cursor.fetchall()

    if produits:
        y_position = 100  # Starting Y position
        padding_x = 500  # Left padding
        table_height = 60  # Height for each table row with progress bar

        # Header row with separators
        header_frame = CTkFrame(tabview.tab("Rupture de stock"), fg_color="white", corner_radius=10, border_width=1)
        canvas2.create_window(padding_x, y_position, anchor="nw", window=header_frame, width=850, height=30)
        CTkLabel(header_frame, text="Nom du produit", text_color="black", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=(20, 10), pady=5)
        CTkLabel(header_frame, text="|", text_color="gray", font=("Arial", 14)).grid(row=0, column=1, padx=5)
        CTkLabel(header_frame, text="Quantité", text_color="black", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=(10, 10), pady=5)
        CTkLabel(header_frame, text="|", text_color="gray", font=("Arial", 14)).grid(row=0, column=3, padx=5)
        CTkLabel(header_frame, text="Niveau de stock", text_color="black", font=("Arial", 14, "bold")).grid(row=0, column=4, padx=(10, 20), pady=5)
        CTkLabel(header_frame, text="|", text_color="gray", font=("Arial", 14)).grid(row=0, column=5, padx=5)
        CTkLabel(header_frame, text="Date de peremption", text_color="black", font=("Arial", 14, "bold")).grid(row=0, column=6, padx=(10, 10), pady=5)

        y_position += 40  # Move down for next rows

        for produit in produits:
            nom, quantite_en_stock, date_peremption = produit

    # Créer un cadre pour chaque ligne de produit
            row_frame = CTkFrame(tabview.tab("Rupture de stock"), fg_color="white", corner_radius=10, border_width=1)
            canvas2.create_window(padding_x, y_position, anchor="nw", window=row_frame, width=850, height=table_height)

    # Afficher le nom du produit
            CTkLabel(row_frame, text=nom, text_color="black", font=("Arial", 12)).grid(row=0, column=0, padx=(20, 10), pady=5)

    # Séparateur vertical
            CTkLabel(row_frame, text="|", text_color="gray", font=("Arial", 12)).grid(row=0, column=1, padx=5)

    # Afficher la quantité
            CTkLabel(row_frame, text=str(quantite_en_stock), text_color="black", font=("Arial", 12)).grid(row=0, column=2, padx=(10, 10), pady=5)

    # Séparateur vertical
            CTkLabel(row_frame, text="|", text_color="gray", font=("Arial", 12)).grid(row=0, column=3, padx=5)

    # Barre de progression pour le niveau de stock
            stock_level = quantite_en_stock / 10  # Ratio pour la barre de progression
            progress_bar = CTkProgressBar(row_frame, width=200, height=10)
            progress_bar.set(stock_level)  # Définir le niveau de la barre
            progress_bar.grid(row=0, column=4, padx=(10, 20), pady=5)

    # Séparateur vertical
            CTkLabel(row_frame, text="|", text_color="gray", font=("Arial", 12)).grid(row=0, column=5, padx=5)

    # Afficher la date de péremption
            CTkLabel(row_frame, text=date_peremption, text_color="black", font=("Arial", 12)).grid(row=0, column=6, padx=(10, 10), pady=5)

    # Avancer la position y pour la prochaine ligne de produit
            y_position += table_height + 10
    else:
        # Message if no product is low on stock
        canvas2.create_text(600, 300, text="Aucun produit en rupture de stock", fill="red", font=("Arial", 16))



# Afficher les produits et vérifier le stock
afficher_stock_et_date_de_peremption()
afficher_tous_les_produits()

app.mainloop()
