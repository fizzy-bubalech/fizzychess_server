from flask import Flask, url_for , Response

from flask_login import UserMixin, login_user, login_required, logout_user, current_user

from server.database import DatabaseQuery

from server import login_manager

from server import app
from server.request_handling import request_handling

@login_manager.user_loader
def load_user(user_id):
    query = DatabaseQuery()
    return query.get_user(int(user_id))

@app.route("/")
def test():
    return('worked')
            
@app.route("/req=<head>#<body>#<meta>")
def request(head,body,meta):
    handler = request_handling()
    if(meta != ''):
        user_id = handler.login_user_handler(meta) #TODO 
        if(user_id == None):
            return 3032
    elif(int(head)== 301):
        user_id = handler.login_request_handling(body)
        if(user_id == None):
            return 3032
    else:
        return 3000
    reqs = {101:handler.queue_req_handling,
            102:handler.queue_req_handling,
            103:handler.queue_req_handling,
            301: handler.login_request_handling}
    if head in reqs.keys():
        return reqs[int(head)](head,body,user_id)
    else: 
        return "Invalid Request Code", 400

@app.errorhandler(404)
def page_not_found(e):
    return "fuck you page not found", 404