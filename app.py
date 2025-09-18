from flask import Flask, render_template, redirect, url_for, request, make_response
import json
import markdown
import uuid
from assets.gestionDB import *

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



if __name__ == '__main__':
    app.run(debug=True)