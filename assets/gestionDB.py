import sqlite3
from sqlite3 import Error
import random


cheminDB="static/data/gamehub.db"

def create_connection(db_file):
    """ crée une connexion à la base de données SQLite
    :param db_file: chemin vers la base de données SQLite
    :return: objet connexion ou None
    """
    connexion = sqlite3.connect(db_file)
    curseur = connexion.cursor()
    return curseur

def execute_query(curseur, query):
    curseur.execute(query)
    result = curseur.fetchall()
    return result

def generate_code():
    """
    Génère un code aléatoire de 4 caractères composé de lettres majuscules et de chiffres.
    Returns:
        str: Un code aléatoire de 4 caractères.
    """

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choices(chars, k=4))


def createPartie(game_id): 
    """
    Crée une nouvelle partie générale dans la table "Parties" avec un code unique.
    """
    curseur = create_connection(cheminDB)
    # Crée une nouvelle partie dans la table "Parties"
    code = generate_code()
    existing_codes = execute_query(curseur, "SELECT GameCode FROM Parties") #On récupère les code déja existants
    while (code,) in existing_codes: #tant que le code existe déjà, on en génère un nouveau
        code = generate_code()
        existing_codes = execute_query(curseur, "SELECT GameCode FROM Parties")
    query = f"INSERT INTO Parties (GameCode, JeuId, EtatLancement, sessionHote) VALUES ('{code}', {game_id}, '0', '{code+'HOTE'}')"
    curseur.execute(query)
    curseur.connection.commit()
    return curseur.lastrowid

def addJoueurToPartie(codePartie, session, pseudo):
    """
    Appelée pour ajouter des jouueurs a une partie existante. (que ce soit le joueur qui rejoins ou qui crée la partie)
    
    Si le couple session/codePartie n'existe pas, on ajoute le joueur a et sa partie a la table générale 



    Vérifie si une partie avec le code donné existe dans la table "Parties".
    Args:
        codePartie (str): Le code de la partie à rejoindre.
    Returns:
        bool: True si la partie existe, False sinon.
    """
    pass