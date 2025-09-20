import sqlite3
from sqlite3 import Error
import random
import datetime

if __name__ == "__main__":
    from ressourcesJeux.AgentTrouble.AgentTroubleFunctions import *
else :
    from static.ressourcesJeux.AgentTrouble.AgentTroubleFunctions import *

cheminDB="static/data/gamehub.db"
connexion=""
def create_connection(db_file):
    """ crée une connexion à la base de données SQLite
    :param db_file: chemin vers la base de données SQLite
    :return: objet connexion ou None
    """
    global connexion
    connexion = sqlite3.connect(db_file)
    curseur = connexion.cursor()
    return curseur

def close_connection():
    """ ferme la connexion à la base de données SQLite
    """
    global connexion
    if connexion:
        connexion.close()

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
    curseur.close()
    close_connection()
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
    query = f"DELETE FROM {tableJoueursJeu} WHERE GameCode = '{codePartie}';"
    curseur.execute(query)
    # Supprimer la partie de la table spécifique au jeu
    query = f"DELETE FROM {tableJeu} WHERE GameCode = '{codePartie}'"
    curseur.execute(query)

    query = f"DELETE FROM Parties WHERE GameCode = '{codePartie}'"
    curseur.execute(query)
    query = f"DELETE FROM Joueurs WHERE GameCode = '{codePartie}'"
    curseur.execute(query)

    curseur.connection.commit()
    curseur.close()
    close_connection()

def createPartie(game_id,sessionHote): 
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
    query = f"INSERT INTO Parties (GameCode, JeuId, EtatLancement, sessionHote, Timestamp) VALUES ('{code}', {game_id}, '0', '{sessionHote}', {timestamp})"
    curseur.execute(query)
    curseur.connection.commit()

    # Supprime les parties dont le timestamp est plus petit que (actuel - 604800), donc les parties datent de + d'une semaine
    seuil = int(datetime.datetime.now().timestamp()) - 604800
    codes_parties = [row[0] for row in execute_query(curseur, f"SELECT GameCode FROM Parties WHERE Timestamp < {seuil}")] #Récupère tous les codes de parties
    for c in codes_parties:
        deletePartie(c)
    curseur.connection.commit()
    curseur.close()

    return code

def getEtatPartieByCode(codePartie):
    """
    Récupère l'état d'une partie en fonction de son code.
    Args:
        codePartie (str): Le code de la partie.
    Returns:
        int: L'état de la partie ('0', '1', '2', 'A', 'F'), ou None si la partie n'existe pas.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT EtatLancement FROM Parties WHERE GameCode = '{codePartie}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    if result:
        return result[0][0]
    return None

def setEtatPartieByCode(codePartie, nouvelEtat):
    """
    Met à jour l'état d'une partie en fonction de son code.
    Args:
        codePartie (str): Le code de la partie.
        nouvelEtat (str): Le nouvel état de la partie ('0', '1', '2', 'A', 'F').
    """
    curseur = create_connection(cheminDB)
    query = f"UPDATE Parties SET EtatLancement = '{nouvelEtat}' WHERE GameCode = '{codePartie}'"
    curseur.execute(query)
    curseur.connection.commit()
    curseur.close()
    close_connection()

def addJoueurToPartie(codePartie, session, pseudo):
    """
    Appelée pour ajouter des jouueurs a une partie existante. (que ce soit le joueur qui rejoins ou qui crée la partie)
    
    Si le couple session/codePartie n'existe pas, on ajoute le joueur a a la table des jouers généraux.
    Si le couple session/codePartie existe déjà, on met juste à jour son pseudo.

    Args:
        codePartie (str): Le code de la partie à rejoindre ou à créer.
        session (str): L'identifiant de session du joueur.
        pseudo (str): Le pseudo du joueur.
    """
    curseur = create_connection(cheminDB)
    # Vérifier si le couple (session, codePartie) existe déjà
    query_check = f"SELECT * FROM Joueurs WHERE session = '{session}' AND GameCode = '{codePartie}'"
    result = execute_query(curseur, query_check)
    if result!= []:
        # Mettre à jour le pseudo si le joueur existe déjà dans la partie
        query_update = f"UPDATE Joueurs SET Pseudo = '{pseudo}' WHERE session = '{session}' AND GameCode = '{codePartie}'"
        curseur.execute(query_update)
    else:
        # Ajouter le joueur à la partie
        query_insert = f"INSERT INTO Joueurs (session, Pseudo, GameCode) VALUES ('{session}', '{pseudo}', '{codePartie}')"
        curseur.execute(query_insert)
    curseur.connection.commit()
    curseur.close()
    close_connection()

def getJoueursByCode(codePartie):
    """
    Récupère la liste des joueurs associés à une partie donnée.
    Args:
        codePartie (str): Le code de la partie.
    Returns:
        list: Une liste de dictionnaires contenant les informations des joueurs (session, pseudo).
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT Pseudo FROM Joueurs WHERE GameCode = '{codePartie}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    joueurs = [x[0] for x in result]
    return joueurs

def getGameIdByCode(codePartie):
    """
    Récupère l'ID du jeu associé à une partie donnée.
    Args:
        codePartie (str): Le code de la partie.
    Returns:
        int: L'ID du jeu associé à la partie, ou None si la partie n'existe pas.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT JeuId FROM Parties WHERE GameCode = '{codePartie}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    if result:
        return result[0][0]
    return None

def getPseudoBySessionAndGameCode(session, gameCode):
    """
    Récupère le pseudo d'un joueur en fonction de son identifiant de session et du code de la partie.
    Args:
        session (str): L'identifiant de session du joueur.
        GameCode (str): Le code de la partie.
    Returns:
        str: Le pseudo du joueur, ou None si le joueur n'existe pas.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT Pseudo FROM Joueurs WHERE session = '{session}' and GameCode = '{gameCode}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    if result:
        return result[0][0]
    return None

def getSessionHoteByGameCode(gameCode):
    """
    Récupère l'identifiant de session de l'hôte d'une partie en fonction du code de la partie.
    Args:
        GameCode (str): Le code de la partie.
    Returns:
        str: L'identifiant de session de l'hôte, ou None si la partie n'existe pas.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT sessionHote FROM Parties WHERE GameCode = '{gameCode}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    if result:
        return result[0][0]
    return None

def getLogsByGameCode(gameCode):
    """
    Récupère les logs d'une partie en fonction du code de la partie.
    Args:
        GameCode (str): Le code de la partie.
    Returns:
        list: Une liste de dictionnaires contenant les informations des logs (timestamp, message).
    """
    curseur = create_connection(cheminDB)
    gameName = execute_query(curseur, f"SELECT GameName FROM Parties JOIN Jeux ON Parties.JeuId = Jeux.Id WHERE GameCode = '{gameCode}'")[0][0]
    tableJoueursJeu = "Joueurs"+gameName  # Nom de la table spécifique au jeu
    
    query = f"SELECT t2.Pseudo, t1.* FROM {tableJoueursJeu} t1, Joueurs t2 WHERE t1.GameCode = '{gameCode}' AND t1.session = t2.session AND t1.GameCode = t2.GameCode"
    resultDonnées = execute_query(curseur, query)
    liste_colonnes = [description[0] for description in curseur.description]
    liste_resultats = [list(row) for row in resultDonnées]
    curseur.close()
    close_connection()
    return liste_colonnes, liste_resultats

def getSessionsByGameCode(gameCode):
    """
    Récupère les sessions des joueurs d'une partie en fonction du code de la partie.
    Args:
        GameCode (str): Le code de la partie.
    Returns:
        list: Une liste de sessions des joueurs.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT session FROM Joueurs WHERE GameCode = '{gameCode}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    sessions = [x[0] for x in result]
    return sessions

def setParamsPartieByCode(codePartie, params):
    """
    Met à jour les paramètres d'une partie en fonction de son code.
    Args:
        codePartie (str): Le code de la partie.
        params (str): Les paramètres de la partie au format JSON.
    """
    curseur = create_connection(cheminDB)
    query = f"UPDATE Parties SET Params = '{params}' WHERE GameCode = '{codePartie}'"
    curseur.execute(query)
    curseur.connection.commit()
    curseur.close()
    close_connection()

def getParamsPartieByCode(codePartie):
    """
    Récupère les paramètres d'une partie en fonction de son code.
    Args:
        codePartie (str): Le code de la partie.
    Returns:
        dict: Les paramètres de la partie au format dictionnaire, ou None si la partie n'existe pas.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT Params FROM Parties WHERE GameCode = '{codePartie}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    if result:
        return result
    return None


def createAgentTroublePartie(GameCode, nbLieux):
    """
    Crée une nouvelle partie du jeu "Agent Trouble" en récupérant les infos de la game et les ajoutant dans la table PartiesAgentTrouble et JoueursAgentTrouble.
    Args:
        GameCode (str): Le code de la partie.
    """
    listeSessions=getSessionsByGameCode(GameCode)#On récupère les sessions des joueurs de la partie
    
    infosPartie, bytesImages=genererPartieAgentTrouble(len(listeSessions),nbLieux,GameCode) #On récupère les infos de la partie AT
    
    dicoFinal={}#Affecte les valeurs des 'items' agent trouble aux sessions
    for i in range(len(listeSessions)): #On lie les sessions aux joueurs d'AT
        session=listeSessions[i]
        dicoFinal[session]=infosPartie[i]
    curseur = create_connection(cheminDB)
    # Ajouter les infos des joueurs à la table "JoueursAgentTrouble"
    for session, infos in dicoFinal.items():

        query_insert = f"INSERT INTO JoueursAgentTrouble (session, lieu, role, carte, GameCode) VALUES ('{session}', '{infos[0].replace("'", "''")}', '{infos[1].replace("'", "''")}', '{infos[2]}', '{GameCode}')"
        curseur.execute(query_insert)
    # Ajouter les infos de la partie à la table "PartiesAgentTrouble"
    query_insert = f"INSERT INTO PartiesAgentTrouble (GameCode, Etat, imagePlateau) VALUES (?, ?, ?)"
    curseur.execute(query_insert, (GameCode, 'A', bytesImages))
    curseur.connection.commit()
    curseur.close()
    close_connection()
    
def getInfosAgentTroubleBySessionAndGameCode(session, gameCode):
    """
    Récupère les informations spécifiques au jeu "Agent Trouble" pour un joueur donné en fonction de son identifiant de session et du code de la partie.
    Args:
        session (str): L'identifiant de session du joueur.
        GameCode (str): Le code de la partie.
    Returns:
        dict: Un dictionnaire contenant les informations du joueur (lieu, role, carte), ou None si le joueur n'existe pas.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT lieu, role, carte FROM JoueursAgentTrouble WHERE session = '{session}' and GameCode = '{gameCode}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    if result:
        return {"lieu": result[0][0], "role": result[0][1], "carte": result[0][2]}
    return None

def getPlateauAgentTroubleByGameCode(gameCode):
    """
    Récupère l'image du plateau de jeu pour une partie donnée du jeu "Agent Trouble".
    Args:
        GameCode (str): Le code de la partie.
    Returns:
        bytes: Les données binaires de l'image du plateau, ou None si la partie n'existe pas.
    """
    curseur = create_connection(cheminDB)
    query = f"SELECT imagePlateau FROM PartiesAgentTrouble WHERE GameCode = '{gameCode}'"
    result = execute_query(curseur, query)
    curseur.close()
    close_connection()
    if result:
        return result[0][0]
    return None