from flask import Flask, render_template
app = Flask(__name__)

from main import Game

def reset_game():
    return Game()

g = reset_game()

@app.route('/')
def home():
    return g.tribes[1].name

@app.route('/list/')
def list():
    g = reset_game()
    return render_template('list.html',title='List',tribes=g.tribes)
