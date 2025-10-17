import os
import json
from dotenv import load_dotenv, set_key
from werkzeug.security import generate_password_hash, check_password_hash

chemin_env="static/.env"

def checkLogin(user, password) :
    user=user.lower()
    #Recuperation du .env
    load_dotenv(chemin_env)
    AdminUsers = json.loads(os.getenv("Admin_Users", "{ }")) #recuperation de la variable, ou initilisation
    if user in AdminUsers and check_password_hash(AdminUsers[user], password) : #si le user existe et que le hash correspond
        return True
    else :
        return False

def addAdmin(user, password):
    user=user.lower()
    load_dotenv(chemin_env) #Ouverture du .env
    AdminUsers = json.loads(os.getenv("Admin_Users", "{ }")) #recuperation de la variable ou initilisation
    if user not in AdminUsers : #Si le use n'existe pas
        AdminUsers[user] = generate_password_hash(password) #on l'enregistre en hashant sont passord
        admin_users_str = json.dumps(AdminUsers) #on transforme en STR
        set_key(chemin_env, "Admin_Users", admin_users_str) #on enregistre
        return True
    else :
        return False
    
