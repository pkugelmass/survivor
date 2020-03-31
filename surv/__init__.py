from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

# import os
# os.chdir(os.path.dirname(__file__))

from surv.game.game import Game

def reset_game():
    return Game()

g = reset_game()

from surv.routes import *
from surv.utils.filters import *
