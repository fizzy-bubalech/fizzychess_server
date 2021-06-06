from flask import Flask

import time

from flask_login import LoginManager

from . import chess
import random
import os



app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24) 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

player_que = []

class Que_item:
    time_format = "3+1"
    rating = "1000"
    cpu = False
    join = True
    match_id = ""
     
    def __init__(self, time_format, rating, cpu, join, user_id):
        self.time_format = time_format
        self.rating = rating
        self.cpu = cpu
        self.join = join
        self.user_id = user_id

class Move_Object:
    game_id = ""
    white = False
    move = "e4"
    start_time = time.time()
    end_time = time.time()

    def __init__(self,white, move, move_n,start_time = time.time(), end_time = time.time(), game_id = int()):
        self.game_id = game_id
        self.white = white
        self.move = move
        self.start_time = start_time
        self.end_time = end_time
        self.move_n = move_n

class Game_Object:

    #TODO add draw offer and add resolution thing
    game_id = int()
    board = chess.Board()
    self_board = [] #the moves along with the times, a stack of move objects 
    black = None #black's id
    white = None #white's id
    w_clock = 60.00*3.00 # black's remaining time on the clock in seconds
    b_clock = 60.00*3.00 # white's remaining time on the clock in seconds 

    #before the game can start black has to confirm start game and white can confirm 
    #and then white's clock starts running and he can play a move
    b_gamestart = False 
    w_gamestart = False

    game_start = 0 #game start time
    n_moves = 0 #the number of moves in the game

    white_turn = True

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

    def push(self, move, start_time, end_time):
        """
        push(slef,move,start_time,end_time)
        """
        self.board.push(move)
        move_object = Move_Object(move,self.white_turn, start_time, end_time,self.game_id)
        if(self.white_turn):
            self.w_clock -= (end_time-start_time)
            if(self.w_clock <= 0):
                pass
                #TODO resolve
        else:
            self.b_clock -= (end_time-start_time)
            if(self.b_clock <= 0):
                pass
                #TODO resolve
        self.self_board.append(move_object)
        self.white_turn = not self.white_turn 

from server import routes