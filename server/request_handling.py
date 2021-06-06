from flask_login.utils import _get_user
from sqlalchemy.orm import query_expression
from sqlalchemy.sql.expression import false, null
from server.functions import search_list, in_que, get_index

from server.database import DatabaseQuery
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

from server import Que_item, Game_Object



class request_handling:
    
    body = ""
    head = 100
    meta = "wow"
    request_type = 0

    query = DatabaseQuery()

    def __init__(self,head = None, body = None,user_id = None) -> None:
        if(head != None):
            self.head = head
            self.body = body
            self.user_id = user_id
            self.request_type = int(self.head[0])

    def handle_request(self):
        handlers = {
            1: self.queue_req_handling,
            2: self.game_request_handling,
            3: self.login_request_handling
        }
        return handlers[int(self.head)](self.head,self.body,self.user_id)

    def queue_req_handling(self, head, body,user_id):
        '''
        This functions handles queue request, 101, 102, 103
        '''
        body = body.split(",")
        player_que = self.query.get_all_queue()
        if int(head) == 101:
            try:
                que_item = Que_item(body[0], body[1], body[2], True, user_id)
                qued = in_que(player_que,que_item)
                if(qued):
                    return "1013,"
                elif(not qued):
                    player_que.append(que_item)
                    self.query.add_queue(que_item)
                    match_index, match_user_id = search_list(player_que,que_item)
                    if(match_index == None):
                        return "1012," 
                    elif(match_index != None):
                        #edit the que item of the matcehd player then remove ur own que item
                        self.query.edit_queue(match_user_id, match_id= user_id)
                        self.query.remove_player_queue(user_id)
                        game = Game_Object(user_id,match_user_id)
                        self.query.add_game(game)
                        game.game_id = self.query.get_game_id_by_object(game)
                        if(game.white == user_id):
                            return f"1011,{game.game_id}|white,"
                        else:
                            return f"1011,{game.game_id}|black,"
            except Exception as e:
                print("General Failure" + e)
                return "1014,"

        
        if(int(head) == 102):
            try:
                que_item = Que_item(body[0], body[1], body[2], True, user_id)
                qued = in_que(player_que,que_item)
                if(not qued):
                    return "1022,"
                if(qued):
                    self.query.remove_player_queue(user_id)
                    player_que.pop(get_index(player_que,que_item))
                    return "1021,"
            except Exception as e:
                print("General Failure" + e)
                return "1023,"

        if(int(head) == 103):
            try:
                que_item = Que_item(body[0], body[1], body[2], True, user_id)
                qued = in_que(player_que,que_item)
                if(not qued):
                    return "1032,"
                if(qued):
                    match_index, match_user_id = search_list(player_que,que_item)
                    if(match_index == None):
                        return "1033,"
                    elif(match_index != None):
                        #edit the que item of the matcehd player then remove ur own que item
                        self.query.edit_queue(match_user_id, match_id= user_id)
                        self.query.remove_player_queue(user_id)
                        game = Game_Object(user_id,match_user_id)
                        self.query.add_game(game)
                        game.game_id = self.query.get_game_id_by_object(game)
                        color = "white" if game.white == user_id else "black"
                        return f"1031,{game.game_id}|{color}"
            except Exception as e:
                print("General Failure" + e)
                return "1034,"

        return f"100,{head},{body}"


    def game_request_handling(self,head,body,user_id):
        '''
        This functions handles game related requests, 201, 202, 203, 204, 205
        '''
        in_game = self.query.get_user_id(user_id) is not None
        user = self.query.get_user_id(user_id)
        if(len(head) != 3):
            return "2000"
        head = head[2]
        if head == 1:
            if()



    def login_user_handler(self, meta):
        info = meta.split("|")
        username = info[0]
        pwd_hash = info[1]
        user = self.query.get_user(username)
        if(user.password == pwd_hash):
            login_user(user,false)
        else: 
            return None
        return user.id


    def login_request_handling(self, body):
        '''
        This functions handles login related requests, 301,302,303
        '''
        info = body.split(",")
        username = info[0]
        pwd_hash = info[1]
        user = self.query.get_user(username)
        if(user.password == pwd_hash):
            login_user(user,false)
        else: 
            return None
        return user.id

    