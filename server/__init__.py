
from flask import Flask, url_for , Response

import os
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24) 

player_que = []

class Que_item:
    time_format = "3+1"
    rating = "1000"
    cpu = False
    def __init__(self, time_format, rating, cpu):
        self.time_format = time_format
        self.rating = rating
        self.cpu = cpu

from server import routes