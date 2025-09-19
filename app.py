from flask import Flask, render_template, redirect, url_for, request, make_response
import json
import markdown
import uuid
from static.gestionDB import *

app = Flask(__name__)

# Configuration des jeux
with open('static/data/games_infos.json', encoding='utf-8') as f:
    GAMES = json.load(f)

for game in GAMES:
    print(game['image'])


@app.route('/')
def index():
    return render_template('index.html', games=GAMES)

@app.route('/game/<int:game_id>') #Description / Règles 
def game_detail(game_id, erreur=""):        
    erreur = request.args.get('erreur', '')
    game = next((g for g in GAMES if g['id'] == game_id), None)
    if game:
        print(game['image'])
        # Convertir le markdown des règles en HTML
        game_copy = game.copy()
        with open(game['rules'], encoding='utf-8') as rules_file:
            rules_md = rules_file.read()
        game_copy['rules_html'] = markdown.markdown(rules_md)
        
        player_id = request.cookies.get("player_id") #On récupère son cookie
        if player_id is None : #Si il n'a pas de cookie
            player_id = str(uuid.uuid4())
            resp = make_response(render_template('game_detail.html', game=game_copy, erreur=erreur))
            resp.set_cookie("player_id", player_id, httponly=True)
            return resp
        
        return render_template('game_detail.html', game=game_copy, erreur=erreur)
    return "Jeu non trouvé", 404


@app.route('/createorjoingame', methods=['POST']) #Transition (pour gerer après un create / join)
def create_or_join():
    pseudo =  request.form['pseudo']
    action = request.form['action']
    codePartie = request.form.get('codePartie', '')
    game_id = request.form.get('game_id', '').upper()
    session = request.cookies.get("player_id") #On récupère son cookie
    if pseudo!="":
        if action == 'create':
            codePartie=createPartie(game_id, session) #Crée une partie dans la DB
            addJoueurToPartie(codePartie, session, pseudo) #Ajoute le joueur qui crée la partie
            return redirect(url_for("index"))
        else :
            if isCodeValid(codePartie):
                addJoueurToPartie(codePartie, session, pseudo) #Ajoute le joueur qui crée la partie
                return redirect(url_for("index"))
            else:
                return redirect(url_for("game_detail", game_id=game_id, erreur="Code de partie invalide"))
    else:
        return redirect(url_for("game_detail", game_id=game_id, erreur="Pseudo invalide"))



@app.route('/<game_code>') #Page de setup ajout des joueurs et de jeu (en fonction de la variable "Etat" dans la DB)
                            #Verifier Cookie sinon envoyer sur la page d'accueil
def game(game_code):
    game_id=getGameIdByCode(game_code)
    game = next((g for g in GAMES if g['id'] == game_id), None)
    session=request.cookies.get("player_id")
    pseudo=getPseudoBySessionAndGameCode(session, game_code)
    hote=getSessionHoteByGameCode(game_code)
    if game :
        game_id=getGameIdByCode(game_code)
        listeJoueurs=getJoueursByCode(game_code)
        
        if session==hote:#Seulement si c'est l'hôte
            nbMinimalJoueurAtteint=game['min_players']<=len(listeJoueurs) #On regarde si le nombre de joueur minimal est atteint
        else:
            nbMinimalJoueurAtteint=False
        if isCodeValid(game_code):
            return render_template("game_lobby.html", game_code=game_code, nbMinimalJoueurAtteint=nbMinimalJoueurAtteint, my_pseudo=pseudo, joueurs=listeJoueurs, game_name=game['title'], game_image=game['image'])
    return "Jeu non trouvé", 404
    

@app.route('/<game_code>/logs') #Page de logs
def game_logs(game_code):
    liste_colonnes, liste_resultats  = getLogsByGameCode(game_code)
    return render_template("game_logs.html", colonnes=liste_colonnes, resultats=liste_resultats)


@app.route('/<game_code>/play') #Page de jeu Agent Trouble
def agent_trouble_game(game_code):
    """
    session = request.cookies.get("player_id")
    
    # Vérifications de base
    if not session or not isCodeValid(game_code):
        return redirect(url_for('index'))
    
    # Récupération des informations du joueur
    pseudo = getPseudoBySessionAndGameCode(session, game_code)
    if not pseudo:
        return redirect(url_for('index'))
    
    # Récupération des données de jeu Agent Trouble
    import base64
    import os
    """
    pseudo = "Joueur1"  # À remplacer par la récupération réelle du pseudo
    imagetest="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"
    # Images par défaut (à remplacer par les vraies données)
    player_card_image = imagetest
    plateau_image = imagetest
    player_role = "Agent"
    lieu = "Lieu"
    # Chargement de l'image plateau (exemple)
    plateau_path = "static/ressourcesJeux/AgentTrouble/assets/Plateau.png"
    
    # Chargement de la carte du joueur (exemple - à adapter selon ta logique)
    # Tu devras implémenter la logique pour récupérer la bonne carte selon le rôle du joueur
    
    return render_template('agent_trouble_game.html', 
                         game_code=game_code,
                         player_name=pseudo,
                         player_card_image=player_card_image,
                         plateau_image=plateau_image,
                         lieu = lieu,
                         player_role=player_role,
                         game_status="Partie en cours",
                         lieu_description="Vue générale du plateau")


if __name__ == '__main__':
    app.run(debug=True)