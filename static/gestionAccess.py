import os
import json
from dotenv import load_dotenv, set_key, dotenv_values
from werkzeug.security import generate_password_hash, check_password_hash

chemin_env="static/.env"

def isThereASecretKey() :
    vals = dotenv_values(chemin_env)
    return bool(vals.get("SECRET_KEY", ""))

def setSecretKey(key) :
    #Enregistrement de la clef secrete
    load_dotenv(chemin_env) #Ouverture du .env
    set_key(chemin_env, "SECRET_KEY", key) #on enregistre

def getSecretKey() :
    vals = dotenv_values(chemin_env)
    return vals.get("SECRET_KEY", "")

def isThereAdmin() :
    vals = dotenv_values(chemin_env)
    AdminUsers = json.loads(vals.get("Admin_Users", "{ }"))
    return len(AdminUsers) > 0

def initAdmin() :
    #Initialisation du compte admin par défaut
    load_dotenv(chemin_env)
    vals = dotenv_values(chemin_env)
    AdminUsers = json.loads(vals.get("Admin_Users", "{ }"))
    AdminUsers["admin"] = generate_password_hash("adminpass") #ajout de l'admin par défaut
    admin_users_str = json.dumps(AdminUsers) #on transforme en STR
    set_key(chemin_env, "Admin_Users", admin_users_str) #on enregistre
    # Met à jour l'environnement du process pour prise en compte immédiate
    os.environ["Admin_Users"] = admin_users_str

def checkLoginAdmin(user, password) :
    user=user.lower()
    vals = dotenv_values(chemin_env)
    AdminUsers = json.loads(vals.get("Admin_Users", "{ }"))
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

