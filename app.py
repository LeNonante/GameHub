from flask import Flask, render_template
import json

app = Flask(__name__)

# Configuration des jeux - vous pouvez modifier ces variables
with open('static/data/games_infos.json', encoding='utf-8') as f:
    GAMES = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', games=GAMES)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    game = next((g for g in GAMES if g['id'] == game_id), None)
    if game:
        return f"<h1>{game['title']}</h1><p>{game['description']}</p>"
    return "Jeu non trouvé", 404

if __name__ == '__main__':
    app.run(debug=True)