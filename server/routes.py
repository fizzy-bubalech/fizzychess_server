from flask import Flask, url_for , Response

from server import app, player_que, Que_item

from server.functions import search_list

@app.route("/")
def test():
    return('worked')

@app.route("/join_queue:<time_format><rating><cpu>") #request for a game with a cpu or a player with specified time format and rating 
#example: "/join_queue:3+1987False"
def queue(time_format,rating,cpu):
    que_item = Que_item(time_format, rating, cpu)
    player_que.append(que_item)