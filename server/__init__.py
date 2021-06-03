from flask import Flask, url_for , Response

import time

from sqlalchemy.sql.expression import true
from sqlalchemy.sql.schema import Index
import chess
import random
import os

from server.functions import search_list, in_que, get_index

from server.database import add_queue, get_all_queue, edit_queue, remove_player_queue, add_game, get_game_id_by_object

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24) 

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
    game_id = int()
    white = False
    move = "e4"
    start_time = time.time()
    end_time = time.time()
    game_id = 0

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

def queue_req_handling(head, body,user_id):
    '''
    This functions handles queue request, 101, 102, 103
    '''
    body = body.split(",")
    player_que = get_all_queue()
    if int(head) == 101:
        try:
            que_item = Que_item(body[0], body[1], body[2], true, user_id)
            qued = in_que(player_que,que_item)
            if(qued):
                return 1013, None
            elif(not qued):
                player_que.append(que_item)
                add_queue(que_item)
                match_index, match_user_id = search_list(player_que,que_item)
                if(match_index == None):
                    return 1012, None
                elif(match_index != None):
                    #edit the que item of the matcehd player then remove ur own que item
                    edit_queue(match_user_id, match_id= user_id)
                    remove_player_queue(user_id)
                    game = Game_Object(user_id,match_user_id)
                    add_game(game)
                    game.game_id = get_game_id_by_object(game)
                    return 1011, game.game_id
        except Exception as e:
            print("General Failure" + e)
            return 1014, None

    
    if(int(head) == 102):
        try:
            que_item = Que_item(body[0], body[1], body[2], true, user_id)
            qued = in_que(player_que,que_item)
            if(not qued):
                return 1022, None
            if(qued):
                remove_player_queue(user_id)
                player_que.pop(get_index(player_que,que_item))
                return 1021, None
        except Exception as e:
            print("General Failure" + e)
            return 1023, None

    if(int(head) == 103):
        try:
            que_item = Que_item(body[0], body[1], body[2], true, user_id)
            qued = in_que(player_que,que_item)
            if(not qued):
                return 1032, None
            if(qued):
                match_index, match_user_id = search_list(player_que,que_item)
                if(match_index == None):
                    return 1033, None
                elif(match_index != None):
                    #edit the que item of the matcehd player then remove ur own que item
                    edit_queue(match_user_id, match_id= user_id)
                    remove_player_queue(user_id)
                    game = Game_Object(user_id,match_user_id)
                    add_game(game)
                    game.game_id = get_game_id_by_object(game)
                    return 1031, game.game_id
        except Exception as e:
            print("General Failure" + e)
            return 1014, None

    return 100, f"100\n{head}: {body}"


from server import routes