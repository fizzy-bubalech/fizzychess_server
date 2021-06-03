from server.functions import search_list, in_que, get_index

from server.database import add_queue, get_all_queue, edit_queue, remove_player_queue, add_game, get_game_id_by_object

from server import Que_item, Game_Object

def queue_req_handling(head, body,user_id):
    '''
    This functions handles queue request, 101, 102, 103
    '''
    body = body.split(",")
    player_que = get_all_queue()
    if int(head) == 101:
        try:
            que_item = Que_item(body[0], body[1], body[2], True, user_id)
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
            que_item = Que_item(body[0], body[1], body[2], True, user_id)
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
            que_item = Que_item(body[0], body[1], body[2], True, user_id)
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