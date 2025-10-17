import os
import json
from dotenv import load_dotenv, set_key
from werkzeug.security import generate_password_hash, check_password_hash

chemin_env="static/.env"

def isThereASecretKey() :
    #Recuperation du .env
    load_dotenv(chemin_env)
    secret_key = os.getenv("SECRET_KEY", "") #recuperation de la variable, ou initilisation
    if secret_key != "" : #si il y a une clef
        return True
    else :
        return False

def setSecretKey(key) :
    #Enregistrement de la clef secrete
    load_dotenv(chemin_env) #Ouverture du .env
    set_key(chemin_env, "SECRET_KEY", key) #on enregistre

def getSecretKey() :
    #Recuperation de la clef secrete
    load_dotenv(chemin_env) #Ouverture du .env
    secret_key = os.getenv("SECRET_KEY", "") #recuperation de la variable, ou initilisation
    return secret_key

def isThereAdmin() :
    #Recuperation du .env
    load_dotenv(chemin_env)
    AdminUsers = json.loads(os.getenv("Admin_Users", "{ }")) #recuperation de la variable, ou initilisation
    if len(AdminUsers) > 0 : #si il y a au moins un admin
        return True
    else :
        return False
    
def initAdmin() :
    #Initialisation du compte admin par défaut
    load_dotenv(chemin_env) #Ouverture du .env
    AdminUsers = json.loads(os.getenv("Admin_Users", "{ }")) #recuperation de la variable, ou initilisation
    AdminUsers["admin"] = generate_password_hash("adminpass") #ajout de l'admin par défaut
    admin_users_str = json.dumps(AdminUsers) #on transforme en STR
    set_key(chemin_env, "Admin_Users", admin_users_str) #on enregistre
    # Met à jour l'environnement du process pour prise en compte immédiate
    os.environ["Admin_Users"] = admin_users_str

def checkLoginAdmin(user, password) :
    user=user.lower()
    #Recuperation du .env
    load_dotenv(chemin_env)
    AdminUsers = json.loads(os.getenv("Admin_Users", "{ }")) #recuperation de la variable, ou initilisation
    if user in AdminUsers and check_password_hash(AdminUsers[user], password) : #si le user existe et que le hash correspond
        return True
    else :
        return False

def changeAdmin(old_password, new_password):
    load_dotenv(chemin_env) #Ouverture du .env
    AdminUsers = json.loads(os.getenv("Admin_Users", "{ }")) #recuperation de la variable ou initilisation
    if checkLoginAdmin("admin", old_password): #On verifie l'ancien mot de passe
        AdminUsers["admin"] = generate_password_hash(new_password) #on met a jour le mot de passe
        admin_users_str = json.dumps(AdminUsers) #on transforme en STR
        set_key(chemin_env, "Admin_Users", admin_users_str) #on enregistre
        # Met à jour l'environnement du process pour que le nouveau mdp soit pris en compte immédiatement
        os.environ["Admin_Users"] = admin_users_str
        return True
    else :
        return False

