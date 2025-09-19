from flask import Flask, request, redirect, make_response
import uuid

app = Flask(__name__)

# Ici ce serait une vraie DB (SQLite par ex.)
players = {}  # {uuid: {"game": "ABC123", "pseudo": "Alice", "carte": None}}

@app.route("/join/<game_code>", methods=["GET", "POST"])
def join_game(game_code):
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        player_id = str(uuid.uuid4())

        # On "inscrit" le joueur en DB
        players[player_id] = {"game": game_code, "pseudo": pseudo, "carte": None}

        # On stocke l'UUID dans un cookie
        resp = make_response("sssss")
        resp.set_cookie("player_id", player_id, httponly=True)
        return resp

    return """
        <form method="post">
            Pseudo: <input name="pseudo">
            <input type="submit" value="Rejoindre">
        </form>
    """

@app.route("/game")
def game():
    player_id = request.cookies.get("player_id")
    if not player_id or player_id not in players:
        return "Tu n'es pas inscrit dans une partie"

    joueur = players[player_id]
    return f"Bonjour {joueur['pseudo']}, ta carte = {joueur['carte'] or 'pas encore distribuée'}"


app.run(debug=True)