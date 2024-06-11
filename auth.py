import tkinter as tk
from tkinter import messagebox
import bcrypt
import subprocess
from pymongo import MongoClient

from app import LibraryManagerApp

# Connexion au serveur MongoDB
client = MongoClient('localhost', 27017)

# Accéder à la base de données
db = client['mongo_database']  # Remarquez le changement d'underscore au lieu de tiret
users_collection = db['users']

# Fonction de hachage du mot de passe
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Fonction de vérification du mot de passe
def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def register():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
        return

    # Vérifier si l'utilisateur existe déjà
    if users_collection.find_one({"username": username}):
        messagebox.showerror("Erreur", "Utilisateur déjà existant")
        return

    hashed = hash_password(password)
    user_data = {
        "username": username,
        "password": hashed
    }

    # Enregistrer l'utilisateur dans la base de données
    users_collection.insert_one(user_data)
    messagebox.showinfo("Succès", "Enregistrement réussi")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
        return

    user = users_collection.find_one({"username": username})
    if user and check_password(user["password"], password):
        messagebox.showinfo("Succès", "Connexion réussie")
        root.destroy()  # Fermer la fenêtre d'authentification
        # subprocess.run(["python", "app.py"])
        app = LibraryManagerApp()
        app.mainloop()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Authentification")

# Configuration de la grille
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# Création des champs de saisie
username_label = tk.Label(root, text="Nom d'utilisateur")
username_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = tk.Label(root, text="Mot de passe")
password_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
password_entry = tk.Entry(root, show="*", width=30)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Boutons d'enregistrement et de connexion
register_button = tk.Button(root, text="S'enregistrer", command=register)
register_button.grid(row=2, column=0, padx=10, pady=10, sticky='e')

login_button = tk.Button(root, text="Se connecter", command=login)
login_button.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# Espacer les boutons du bas de la fenêtre
bottom_spacer = tk.Label(root)
bottom_spacer.grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()
