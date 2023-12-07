from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "SuuuuuuperSeaaaaakret"

boggle_game = Boggle()

@app.route("/")
def creating_board():
    """ Create a board """
    board = boggle_game.make_board()
    session["board"] = board
    return render_template("home.html", board= board)

@app.route("/word-check")
def word_check():
    """Check the axios request: word on the server"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route("/end-game", methods=["POST"])
def end_game():
    """saving score, updating highscore and track num of games played"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    number_of_plays = session.get("number_of_plays", 0)

    session["highscore"] = max (score, highscore)
    session["number_of_plays"] = number_of_plays + 1

    return jsonify (record= score > highscore)

    


