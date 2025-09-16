from flask import Flask, render_template, redirect, url_for, request
import json
import markdown

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
def game_detail(game_id):
    game = next((g for g in GAMES if g['id'] == game_id), None)
    if game:
        print(game['image'])
        # Convertir le markdown des règles en HTML
        game_copy = game.copy()
        with open(game['rules'], encoding='utf-8') as rules_file:
            rules_md = rules_file.read()
        game_copy['rules_html'] = markdown.markdown(rules_md)
        return render_template('game_detail.html', game=game_copy)
    return "Jeu non trouvé", 404


@app.route('/createorjoingame', methods=['POST']) #Transition (pour gerer après un create / join)
def create_or_join():
    data = request.get_json()
    print("eee")
    if data["pseudo"]!="":
        #if action=="create":
         return redirect(url_for("/game/1"))
    else :
        return redirect(url_for("/game/3"))



@app.route('/game/<game_code>') #Page de setup ajout des joueurs et de jeu (en fonction de la variable "Etat" dans la DB)
def game(game_code):
    game = next((g for g in GAMES if g['id'] == game_code), None)
    if game:
        return f"<h1>{game['title']}</h1><p>{game['description']}</p>"
    return "Jeu non trouvé", 404

@app.route('/game/<game_code>/logs') #Page de logs
def game_logs(game_code):
    #game = next((g for g in GAMES if g['id'] == game_code), None)
    logs = [[1, 2, 3], [4, 5, 6]]
    game=True
    if game:
        return render_template('game_logs.html', logs=logs, game_code=game_code)
    return "Jeu non trouvé", 404





if __name__ == '__main__':
    app.run(debug=True)