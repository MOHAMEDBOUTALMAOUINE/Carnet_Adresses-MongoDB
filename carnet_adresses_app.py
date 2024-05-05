# copyright BOUTALMAOUINE MOHAMED & AHOUARI BELAID 
import pymongo
import tkinter as tk
from tkinter import messagebox

# Connexion à MongoDB
def connecter_mongodb():
    global collection
    url = entry_url.get()
    database_name = entry_database.get()
    collection_name = entry_collection.get()
    
    try:
        client = pymongo.MongoClient(url)
        database = client[database_name]
        collection = database[collection_name]
        messagebox.showinfo("Connexion réussie", "Connexion à MongoDB établie avec succès.")
        initialiser_interface_crud()
    except pymongo.errors.ConnectionFailure:
        messagebox.showerror("Erreur de connexion", "Impossible de se connecter à MongoDB. Vérifiez l'URL et réessayez.")

# Initialiser l'interface CRUD
def initialiser_interface_crud():
    frame_connexion.destroy()
    
    global entry_nom, entry_prenom, entry_telephone, entry_email, entry_adresse, entry_recherche
    
    frame_crud_contacts = tk.Frame(root)
    frame_crud_contacts.pack(pady=10)

    label_nom = tk.Label(frame_crud_contacts, text="Nom:")
    label_nom.grid(row=0, column=0, padx=5, pady=5)
    entry_nom = tk.Entry(frame_crud_contacts)
    entry_nom.grid(row=0, column=1, padx=5, pady=5)

    label_prenom = tk.Label(frame_crud_contacts, text="Prénom:")
    label_prenom.grid(row=1, column=0, padx=5, pady=5)
    entry_prenom = tk.Entry(frame_crud_contacts)
    entry_prenom.grid(row=1, column=1, padx=5, pady=5)

    label_telephone = tk.Label(frame_crud_contacts, text="Téléphone:")
    label_telephone.grid(row=2, column=0, padx=5, pady=5)
    entry_telephone = tk.Entry(frame_crud_contacts)
    entry_telephone.grid(row=2, column=1, padx=5, pady=5)

    label_email = tk.Label(frame_crud_contacts, text="Email:")
    label_email.grid(row=3, column=0, padx=5, pady=5)
    entry_email = tk.Entry(frame_crud_contacts)
    entry_email.grid(row=3, column=1, padx=5, pady=5)

    label_adresse = tk.Label(frame_crud_contacts, text="Adresse:")
    label_adresse.grid(row=4, column=0, padx=5, pady=5)
    entry_adresse = tk.Entry(frame_crud_contacts)
    entry_adresse.grid(row=4, column=1, padx=5, pady=5)

    btn_creer_contact = tk.Button(frame_crud_contacts, text="Créer Contact", command=creer_contact)
    btn_creer_contact.grid(row=5, columnspan=2, padx=5, pady=5)

    frame_actions = tk.Frame(root)
    frame_actions.pack(pady=10)

    btn_lire_tous_contacts = tk.Button(frame_actions, text="Afficher tous les contacts", command=lire_tous_contacts)
    btn_lire_tous_contacts.grid(row=0, column=0, padx=5, pady=5)

    btn_mettre_a_jour_contact = tk.Button(frame_actions, text="Mettre à jour un contact", command=mettre_a_jour_contact)
    btn_mettre_a_jour_contact.grid(row=0, column=1, padx=5, pady=5)

    btn_supprimer_contact = tk.Button(frame_actions, text="Supprimer un contact", command=supprimer_contact)
    btn_supprimer_contact.grid(row=0, column=2, padx=5, pady=5)

    label_recherche = tk.Label(frame_actions, text="Rechercher:")
    label_recherche.grid(row=1, column=0, padx=5, pady=5)
    entry_recherche = tk.Entry(frame_actions)
    entry_recherche.grid(row=1, column=1, padx=5, pady=5)

    btn_rechercher_contact = tk.Button(frame_actions, text="Rechercher", command=rechercher_contact)
    btn_rechercher_contact.grid(row=1, column=2, padx=5, pady=5)

# Opérations CRUD

def creer_contact():
    nom = entry_nom.get()
    prenom = entry_prenom.get() # Nouvelle ligne pour récupérer le prénom
    telephone = entry_telephone.get()
    email = entry_email.get()
    adresse = entry_adresse.get()
    
    contact = {"nom": nom, "prenom": prenom, "telephone": telephone, "email": email, "adresse": adresse}
    collection.insert_one(contact)
    messagebox.showinfo("Succès", "Contact créé avec succès.")

def lire_tous_contacts():
    contacts = list(collection.find())
    if contacts:
        affichage = ""
        for contact in contacts:
            affichage += "Nom: {}\n".format(contact.get('nom', ''))
            affichage += "Prénom: {}\n".format(contact.get('prenom', ''))
            affichage += "Téléphone: {}\n".format(contact.get('telephone', ''))
            affichage += "Email: {}\n".format(contact.get('email', ''))
            affichage += "Adresse: {}\n\n".format(contact.get('adresse', ''))
        messagebox.showinfo("Liste des contacts", affichage)
    else:
        messagebox.showinfo("Liste des contacts", "Aucun contact trouvé.")


def mettre_a_jour_contact():
    nom = entry_nom.get()
    prenom = entry_prenom.get() # Nouvelle ligne pour récupérer le prénom
    telephone = entry_telephone.get()
    email = entry_email.get()
    adresse = entry_adresse.get()
    
    query = {"nom": nom, "prenom": prenom} # Ajout du prénom dans la recherche du contact à mettre à jour
    new_values = {"$set": {"telephone": telephone, "email": email, "adresse": adresse}}
    collection.update_one(query, new_values)
    messagebox.showinfo("Succès", "Contact mis à jour avec succès.")

def supprimer_contact():
    nom = entry_nom.get()
    prenom = entry_prenom.get() # Nouvelle ligne pour récupérer le prénom
    query = {"nom": nom, "prenom": prenom} # Ajout du prénom dans la recherche du contact à supprimer
    collection.delete_one(query)
    messagebox.showinfo("Succès", "Contact supprimé avec succès.")

def rechercher_contact():
    recherche = entry_recherche.get()
    query = {"$or": [{"nom": {"$regex": recherche}},
                     {"prenom": {"$regex": recherche}}, # Ajout de la recherche par prénom
                     {"telephone": {"$regex": recherche}},
                     {"email": {"$regex": recherche}},
                     {"adresse": {"$regex": recherche}}]}
    contacts = list(collection.find(query))
    if contacts:
        affichage = "\n".join([f"Nom: {contact['nom']}\nPrénom: {contact['prenom']}\nTéléphone: {contact['telephone']}\nEmail: {contact['email']}\nAdresse: {contact['adresse']}\n" for contact in contacts])
        messagebox.showinfo("Résultat de la recherche", affichage)
    else:
        messagebox.showinfo("Résultat de la recherche", "Aucun contact trouvé.")

# Interface utilisateur Tkinter
root = tk.Tk()
root.title("Carnet d'adresses")

frame_connexion = tk.Frame(root)
frame_connexion.pack(pady=10)

label_url = tk.Label(frame_connexion, text="URL MongoDB:")
label_url.grid(row=0, column=0, padx=5, pady=5)
entry_url = tk.Entry(frame_connexion)
entry_url.grid(row=0, column=1, padx=5, pady=5)

label_database = tk.Label(frame_connexion, text="Nom de la base de données:")
label_database.grid(row=1, column=0, padx=5, pady=5)
entry_database = tk.Entry(frame_connexion)
entry_database.grid(row=1, column=1, padx=5, pady=5)

label_collection = tk.Label(frame_connexion, text="Nom de la collection:")
label_collection.grid(row=2, column=0, padx=5, pady=5)
entry_collection = tk.Entry(frame_connexion)
entry_collection.grid(row=2, column=1, padx=5, pady=5)

btn_connecter = tk.Button(frame_connexion, text="Connecter à MongoDB", command=connecter_mongodb)
btn_connecter.grid(row=3, columnspan=2, padx=5, pady=5)

root.mainloop()
