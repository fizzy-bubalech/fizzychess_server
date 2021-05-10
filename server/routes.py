from flask import Flask, url_for , Response

from server import app, player_que, Que_item

from server.functions import search_list, in_que, get_index

from server.database import add_queue, get_all_queue, edit_queue 

@app.route("/")
def test():
    return('worked')

@app.route("/join_queue:<time_format><rating><cpu><join><user_id>") #request for a game with a cpu or a player with specified time format and rating 
#example: "/join_queue:3+1987False"
def queue(time_format,rating,cpu,join,user_id):
    que_item = Que_item(time_format, rating, cpu, join, user_id)
    player_que = get_all_queue()
    qued = in_que(player_que,que_item)
    if(not join and qued):
        player_que.pop(get_index(player_que,que_item))
    elif(join and qued):
        player_que.pop(get_index(player_que,que_item))
        remove_player_queue(user_id)
        return "ERROR ALREADY IN QUEUE"
    elif(join and not qued):
        player_que.append(que_item)
        add_queue(que_item) 
        match_index, match_user_id = search_list(player_queue,que_item)
        if(match == None):
            return "STILL LOOKING..."
        else:
            edit_queue(match_user_id, match_id= user_id)
            remove_player_queue(user_id)
            """Todo: make game object and start the thing"""
            
            
