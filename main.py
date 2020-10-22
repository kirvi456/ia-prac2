from flask import Flask, request, render_template
from game.game import Game

app = Flask(__name__, template_folder='template')
game = Game()

@app.route("/")
def main():
    playerTurn = request.args.get('turno')
    matrixState = request.args.get('estado')
    return game.CalcMove(4,"1" if playerTurn == "0" else "2" ,matrixState+"")

if __name__ == "__main__":
    app.run()