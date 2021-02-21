
from flask import Flask, url_for , Response

import chess
import random
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24) 

player_que = []

class Que_item:
    time_format = "3+1"
    rating = "1000"
    cpu = False
    join = True
     
    def __init__(self, time_format, rating, cpu, join, user_id):
        self.time_format = time_format
        self.rating = rating
        self.cpu = cpu
        self.join = join
        self.user_id = user_id

class Game:
    board = chess.Board()
    black = None
    white = None
    w_clock = 0
    b_clock = 0
    b_gamestart = False
    w_gamestart = False
    game_start = 0
    def __init__(self, player_1, player_2):
        coin_flip = random.randint(1, 2)
        if(coin_flip == 1):
            self.white = player_1
            self.black = player_2
        else:
            self.white = player_2
            self.black = player_1
    def player_ready(self,player):
        if(player == self.white and self.b_gamestart):
            self.w_gamestart = True
            #TODO start the game
        elif(player != self.white):
            self.b_gamestart = True



from server import routes