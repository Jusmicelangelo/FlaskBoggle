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


    


