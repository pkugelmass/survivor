from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'wow'

from surv.routes import *
from surv.utils.filters import *
