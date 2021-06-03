from flask import Flask, url_for , Response

from server import app, player_que, Que_item, queue_req_handling

@app.route("/")
def test():
    return('worked')
            
@app.route("/req=<head>#<body>#<meta>")
def request(head,body,meta):
    user_id =int() #TODO 
    reqs = {101:queue_req_handling,
            102:queue_req_handling,
            103:queue_req_handling}
    if head in reqs.keys():
        return reqs[int(head)](head,body,user_id)
    else: 
        return "Invalid Request Code"