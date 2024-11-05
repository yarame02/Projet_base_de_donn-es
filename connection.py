from tkinter import *
from tkinter import messagebox
import mysql.connector

root=Tk()
root.title('login')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False, False)

img=PhotoImage(file='')
Label(root, image=img, bg = 'white').place(x=50,y=50)

frame=Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Se connecter', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_enter(e):
    user.delete(0, 'end')
def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Nom utilisateur')

user = Entry(frame, width = 25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0,'Nom utilisateur')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25,y=107)

def on_enter(e):
    code.delete(0, 'end')
def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Nom utilisateur')
def connect():
    username = user.get()
    password = code.get()

    # Connexion à la base de données MySQL
    try:
        conn = mysql.connector.connect(
            host='localhost',         # Adresse du serveur MySQL
            user='root', # Nom d'utilisateur MySQL
            password='', # Mot de passe MySQL
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
            import interface_admin  # Importez et lancez le module de l'interface admin
        else:
            messagebox.showerror('Erreur', 'Nom d\'utilisateur ou mot de passe incorrect')
    except mysql.connector.Error as err:
        messagebox.showerror('Erreur', f'Erreur de connexion à la base de données : {err}')
code = Entry(frame, width = 25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0,'Mot de passe')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25,y=177)

Button(frame, width=39, pady=7, text='se connecter', bg='#57a1f8', fg='white', border=0, command=connect).place(x=35, y=204)
root.mainloop()
