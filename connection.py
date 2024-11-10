import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import mysql.connector

# Fonction pour la connexion à la base de données
def connect():
    username = user.get()
    password = code.get()

    # Connexion à la base de données MySQL
    try:
        conn = mysql.connector.connect(
            host='localhost',         # Adresse du serveur MySQL
            user='root',              # Nom d'utilisateur MySQL
            password='',              # Mot de passe MySQL
            database='pharmacie'      # Nom de la base de données
        )
        cursor = conn.cursor()
        query = 'SELECT * FROM gestion_pharmacie_utilisateur WHERE nom_utilisateur = %s AND mot_de_passe = %s'
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            # L'utilisateur est authentifié, ouvrez l'interface admin
            root.destroy()  # Ferme la fenêtre de connexion
            import administration  # Importez et lancez le module de l'interface admin
        else:
            messagebox.showerror('Erreur', 'Nom d\'utilisateur ou mot de passe incorrect')
    except mysql.connector.Error as err:
        messagebox.showerror('Erreur', f'Erreur de connexion à la base de données : {err}')

# Créer la fenêtre principale
root = tk.Tk()
root.title("Login Page")
root.geometry("1600x800")
root.configure(bg="white")

# Charger l'image de fond (personnalisez le chemin avec votre image)
bg_image = Image.open("medoc.jpg")
bg_image = bg_image.resize((800, 800), Image.Resampling.LANCZOS)  # Adapter la taille de l'image
bg_photo = ImageTk.PhotoImage(bg_image)

# Ajouter un cadre pour l'image de fond
bg_frame = tk.Frame(root, width=800, height=800)
bg_frame.grid(row=0, column=0)
bg_label = tk.Label(bg_frame, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Ajouter le cadre de connexion
login_frame = tk.Frame(root, width=800, height=800, bg="white")
login_frame.grid(row=0, column=1, sticky="nsew")
login_frame.grid_propagate(False)

# Titre "Login"
title_font = font.Font(family="Helvetica", size=32, weight="bold")
title_label = tk.Label(login_frame, text="Login", font=title_font, bg="white")
title_label.grid(row=0, column=0, pady=(30, 10), sticky="w", padx=60)

# Champs Email et Mot de passe
email_label = tk.Label(login_frame, text="Email Address", bg="white", font=('Helvetica', 14))
email_label.grid(row=1, column=0, padx=60, pady=(10, 0), sticky="w")
user = tk.Entry(login_frame, width=30, font=('Helvetica', 14))
user.grid(row=2, column=0, padx=60, pady=5)

password_label = tk.Label(login_frame, text="Password", bg="white", font=('Helvetica', 14))
password_label.grid(row=3, column=0, padx=60, pady=(10, 0), sticky="w")
code = tk.Entry(login_frame, show="*", width=30, font=('Helvetica', 14))
code.grid(row=4, column=0, padx=60, pady=5)

# Lien "Forgot Password?"
forgot_label = tk.Label(login_frame, text="Forgot Password?", fg="blue", bg="white", font=('Helvetica', 12), cursor="hand2")
forgot_label.grid(row=5, column=0, padx=60, pady=(5, 20), sticky="w")

# Bouton de connexion
login_button = tk.Button(login_frame, text="LOGIN", bg="blue", fg="white", width=20, font=('Helvetica', 14), command=connect)
login_button.grid(row=6, column=0, padx=60, pady=10)

# Options de connexion avec des services externes
or_label = tk.Label(login_frame, text="Or sign up with", bg="white", font=('Helvetica', 14))
or_label.grid(row=7, column=0, padx=60, pady=(20, 5))

# Boutons de connexion via Google, Apple, Microsoft
google_button = tk.Button(login_frame, text="Sign in with Google", width=25, bg="white", anchor="w", font=('Helvetica', 12))
google_button.grid(row=8, column=0, padx=60, pady=2)

apple_button = tk.Button(login_frame, text="Sign in with Apple", width=25, bg="white", anchor="w", font=('Helvetica', 12))
apple_button.grid(row=9, column=0, padx=60, pady=2)

microsoft_button = tk.Button(login_frame, text="Sign in with Microsoft", width=25, bg="white", anchor="w", font=('Helvetica', 12))
microsoft_button.grid(row=10, column=0, padx=60, pady=2)

# Démarrer la boucle principale
root.mainloop()
