from flask import Flask, render_template, redirect, url_for, request, make_response, session
import json
import markdown
import uuid
from static.gestionDB import *
from static.gestionAccess import *
import base64
import os
import shutil
from functools import wraps

app = Flask(__name__)

# Configuration des jeux
with open('static/data/games_infos.json', encoding='utf-8') as f:
    GAMES = json.load(f)
    
db_path = 'static/data/gamehub.db'
db_template = 'static/data/gamehub_vierge.db'

if not os.path.exists(db_path):
    shutil.copy(db_template, db_path)

if not isThereAdmin():
    initAdmin()

if not isThereASecretKey(): #Si pas de clef secrete (utilisée pour les sessions)
    # Générer une clé secrète aléatoire et la stocker dans le .env
    secret_key = os.urandom(24).hex()
    setSecretKey(secret_key)#Enregistrer la clef dans le .env
    app.secret_key=secret_key #Enregistrer la clef dans l'app
else :
    app.secret_key=getSecretKey() #Lire la clef dans le .env et l'enregistrer dans l'app

@app.route('/')
def index():
    print(GAMES)
    return render_template('index.html', games=GAMES)

@app.route('/game/<int:game_id>') #Description / Règles 
def game_detail(game_id, erreur=""):        
    erreur = request.args.get('erreur', '')
    game = next((g for g in GAMES if g['id'] == game_id), None)
    if game:
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
            return redirect(url_for("game", game_code=codePartie))
        else :
            if isCodeValid(codePartie):
                if getEtatPartieByCode(codePartie)!=0: #Si la partie n'est pas en état "en attente"
                    return redirect(url_for("game_detail", game_id=game_id, erreur="La partie a déjà commencé ou est terminée"))
                else :
                    addJoueurToPartie(codePartie, session, pseudo) #Ajoute le joueur qui crée la partie
                    return redirect(url_for("game", game_code=codePartie))
            else:
                return redirect(url_for("game_detail", game_id=game_id, erreur="Code de partie invalide"))
    else:
        return redirect(url_for("game_detail", game_id=game_id, erreur="Pseudo invalide"))
    
    
@app.route('/lancementgame', methods=['POST']) #Transition (pour lancer la config de la partie)
def lancementgame():

    codePartie = request.form.get('gameCode', '')
    game_id=getGameIdByCode(codePartie)
    
    if game_id == 1 : #Agent trouble
        nb_lieux = request.form.get('nb_lieux', 30)
        if nb_lieux.isdigit() and 2 <= int(nb_lieux) <= 30:
            nb_lieux = int(nb_lieux)
        elif int(nb_lieux) >30:
            nb_lieux = 30  # Valeur par défaut
        else:
            nb_lieux = 2  # Valeur minimale
        params=[nb_lieux]

    
    params_text = json.dumps(params)  # Convertir la liste en chaîne JSON
    setParamsPartieByCode(codePartie, params_text)  # Enregistrer les
    setEtatPartieByCode(codePartie, 1) #On passe l'état de la partie à "lancée"
    return redirect(url_for("game",game_code=codePartie))



@app.route('/<game_code>') #Page de setup ajout des joueurs et de jeu (en fonction de la variable "Etat" dans la DB)
                            #Verifier Cookie sinon envoyer sur la page d'accueil
def game(game_code):#param est fourni quand cette fonction est lancée pour configurer la partie (par lancementgame)
    game_id=getGameIdByCode(game_code)
    hote=getSessionHoteByGameCode(game_code)
    session=request.cookies.get("player_id")
    if (getEtatPartieByCode(game_code)==0 ) or (getEtatPartieByCode(game_code)==1 and session!=hote): #Si la partie est pas encore lancée
        if session not in getSessionsByGameCode(game_code): #Si le joueur n'est pas dans la partie, on le redirige
            return redirect(url_for('game_detail', game_id=game_id, erreur="Vous n'êtes pas dans cette partie"))
        
        game = next((g for g in GAMES if g['id'] == game_id), None)
        pseudo=getPseudoBySessionAndGameCode(session, game_code)
        if game :
            game_id=getGameIdByCode(game_code)
            listeJoueurs=getJoueursByCode(game_code)
            
            if session==hote:#Seulement si c'est l'hôte
                nbMinimalJoueurAtteint=game['min_players']<=len(listeJoueurs) #On regarde si le nombre de joueur minimal est atteint
            else:
                nbMinimalJoueurAtteint=False
            if isCodeValid(game_code):
                IsJoueurHost= session==hote
                game_params=game["params"]
                return render_template("game_lobby.html", game_code=game_code, nbMinimalJoueurAtteint=nbMinimalJoueurAtteint, my_pseudo=pseudo, joueurs=listeJoueurs, game_name=game['title'], game_image=game['image'], game_params=game_params, IsJoueurHost=IsJoueurHost)
        return "Jeu non trouvé", 404
    
    elif getEtatPartieByCode(game_code)==1 and session==hote: #Si la partie a été lancée, on lance la config pour l'hote
        game = next((g for g in GAMES if g['id'] == game_id), None)
        if game :
            if isCodeValid(game_code):
                if game_id==1:
                    params_brut=getParamsPartieByCode(game_code)[0][0] #On récupère les paramètres de la partie (ici le nombre de lieux)
                    params=json.loads(params_brut) #transforme en liste
                    nb_lieux=params[0] #On récupère le nombre de lieux
                    createAgentTroublePartie(game_code, nb_lieux) #On crée la partie Agent Trouble dans la DB
                    setEtatPartieByCode(game_code, 2) #On passe l'état de la partie à "configurée"
                    return redirect(url_for('game', game_code=game_code))
                else:
                    return "Page de jeu non encore disponible"
        return "Jeu non trouvé", 404
    
    elif getEtatPartieByCode(game_code)==2: #Si la partie est configurée, on lance le jeu
        game = next((g for g in GAMES if g['id'] == game_id), None)
        if game :
            if isCodeValid(game_code):
                if game_id==1:
                        session = request.cookies.get("player_id")
                        # Vérifications de base
                        if not session or not isCodeValid(game_code):
                            return redirect(url_for('index'))
                        
                        # Récupération des informations du joueur
                        pseudo = getPseudoBySessionAndGameCode(session, game_code)
                        if not pseudo:
                            return redirect(url_for('index'))
                        
                        infos_joueurs = getInfosAgentTroubleBySessionAndGameCode(session, game_code)

                        # Images par défaut
                        player_card_image = infos_joueurs['carte']
                        player_role = infos_joueurs['role']
                        lieu = infos_joueurs['lieu']
                        
                        # Chargement de l'image plateau
                        plateau_image_bytes = getPlateauAgentTroubleByGameCode(game_code)
                        plateau_image = base64.b64encode(plateau_image_bytes).decode('utf-8')
                        
                        return render_template('agent_trouble_game.html', 
                                            game_code=game_code,
                                            player_name=pseudo,
                                            player_card_image=player_card_image,
                                            plateau_image=plateau_image,
                                            lieu = lieu,
                                            player_role=player_role,
                                            game_status="Partie en cours",
                                            lieu_description="Vue générale du plateau")
                else:
                    return "Page de jeu non encore disponible"
        return "Jeu non trouvé", 404


def login_required(f): #Création d'un décorateur pour les pages admin. Si pas connecté, redirige vers la page de login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function    

@app.route('/<game_code>/logs') #Page de logs
@login_required
def game_logs(game_code):
    liste_colonnes, liste_resultats  = getLogsByGameCode(game_code)
    return render_template("game_logs.html", colonnes=liste_colonnes, resultats=liste_resultats)



@app.route("/login", methods=["GET", "POST"]) #Page de login admin
def login():
    if request.method == "POST":
        pseudo = request.form["pseudo"].lower()
        mdp = request.form["password"]

        if checkLoginAdmin(pseudo, mdp):
            session["user"] = pseudo
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", erreur="Identifiants invalides")

    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    parties=getAllPartiesForAdminPanel()
    if request.method == "POST":
        if request.form.get("action")=="changeAdminPassword":
            old_password = request.form["old_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]
            if new_password != confirm_password:
                return render_template("admin.html", changePasswordError="Les nouveaux mots de passe ne correspondent pas", parties=parties)
            if not checkLoginAdmin(session["user"], old_password):
                return render_template("admin.html", changePasswordError="Ancien mot de passe incorrect", parties=parties)
            
            if checkLoginAdmin(session["user"], old_password):
                changeAdmin(old_password, new_password)
                return render_template("admin.html", changePasswordMessage="Mot de passe changé avec succès", parties=parties)

        if request.form.get("action")=="resetDB":
            resetDB()
            return render_template("admin.html", parties=parties)
        
        if request.form.get("action")=="deletePartie":
            game_code=request.form.get("gameCode", '')
            deletePartie(game_code)
            return render_template("admin.html", parties=parties)
        
        if request.form.get("action")=="logs":
            game_code=request.form.get("gameCode", '')
            return redirect(url_for("game_logs", game_code=game_code))
            
    return render_template("admin.html", parties=parties)

@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)