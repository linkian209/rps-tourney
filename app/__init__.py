'''
This module contains the Flask Application.
'''
from flask import Flask, render_template
from app.api import api_bp
import numpy as np

app = Flask(__name__,static_folder="../static", template_folder="../templates")
app.register_blueprint(api_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view/q_table')
def view_q_table():
    q_table = np.load('winner_q_table.npy')
    return render_template('q_table.html', q_table=q_table)