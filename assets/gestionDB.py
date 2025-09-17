import sqlite3
from sqlite3 import Error
import random
import datetime


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


def isCodeValid(codePartie):
    """
    Vérifie si une partie avec le code donné existe dans la table "Parties".
    Args:
        codePartie (str): Le code de la partie à rejoindre.
    Returns:
        bool: True si la partie existe, False sinon.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT * FROM Parties WHERE GameCode = '{codePartie}'"
    result = execute_query(curseur, query)
    return len(result) > 0

def deletePartie(codePartie):
    """
    Supprime une partie de la table "Parties" et de la table spécifique a son jeu, ainsi que ses joueurs de la table joueurs générale et celle spécifique à son jeu en fonction du code de la partie.
    Args:
        codePartie (str): Le code de la partie à supprimer.
    """
    curseur = create_connection(cheminDB)
    NomJeu=execute_query(curseur, f"SELECT GameName FROM Parties JOIN Jeux ON Parties.JeuId = Jeux.Id WHERE GameCode = '{codePartie}'")[0][0]
    tableJeu = "Parties"+NomJeu  # Nom de la table spécifique au jeu
    tableJoueursJeu = "Joueurs"+NomJeu  # Nom de la table spécifique au jeu
    
    # Supprimer les joueurs de la table spécifique au jeu
    query = f"DELETE FROM {tableJoueursJeu} WHERE session IN ( SELECT Joueurs.session FROM Joueurs WHERE Joueurs.GameCode = '{codePartie}');"
    curseur.execute(query)
    # Supprimer la partie de la table spécifique au jeu
    query = f"DELETE FROM {tableJeu} WHERE GameCode = '{codePartie}'"
    curseur.execute(query)

    query = f"DELETE FROM Parties WHERE GameCode = '{codePartie}'"
    curseur.execute(query)
    query = f"DELETE FROM Joueurs WHERE GameCode = '{codePartie}'"
    curseur.execute(query)

    curseur.connection.commit()

def createPartie(game_id): 
    """
    Crée une nouvelle partie générale dans la table "Parties" avec un code unique.
    """
    curseur = create_connection(cheminDB)
    # Crée une nouvelle partie dans la table "Parties"
    code = generate_code()
    timestamp = int(datetime.datetime.now().timestamp()) #ts en secondes
    existing_codes = execute_query(curseur, "SELECT GameCode FROM Parties") #On récupère les code déja existants
    while (code,) in existing_codes: #tant que le code existe déjà, on en génère un nouveau
        code = generate_code()
        existing_codes = execute_query(curseur, "SELECT GameCode FROM Parties")
    query = f"INSERT INTO Parties (GameCode, JeuId, EtatLancement, sessionHote, Timestamp) VALUES ('{code}', {game_id}, '0', '{code+'HOTE'}', {timestamp})"
    curseur.execute(query)
    curseur.connection.commit()

    # Supprime les parties dont le timestamp est plus petit que (actuel - 604800), donc les parties datent de + d'une semaine
    seuil = int(datetime.datetime.now().timestamp()) - 604800
    codes_parties = [row[0] for row in execute_query(curseur, f"SELECT GameCode FROM Parties WHERE Timestamp < {seuil}")] #Récupère tous les codes de parties
    for code in codes_parties:
        deletePartie(code)
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
