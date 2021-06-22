from sqlalchemy.sql.expression import false
from server.model import Base, Move, Game, User, Queue, or_

from server import Game_Object, Move_Object, Que_item

#imports for the sqlalchemy libary 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Creates the database session
class DatabaseQuery:
	
	def __init__(self) -> None:
		pass
	def make_session():
		engine = create_engine('sqlite:///database.db')
		Base.metadata.create_all(engine)
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		return session

	def add_game(self, game_object):
		session = self.make_session()
		game = Game(
			game_object.white,
			game_object.black,
			game_object.board,
			game_object.n_moves,
			game_object.white_turn,
			game_object.start_time,
			game_object.completed,
			game_object.b_gamestart,
			game_object.w_gamestart)
		session.add(game)
		session.commit()

	def get_game_id_by_object(self,game_object):
		session = self.make_session()
		game = session.query(Game).filet(start_time = game_object.game_start, black_id = game_object.black, white_id = game_object.white).first() 
		return game.id
	def get_game(self,id):
		'''
		This function gets a game by id and then converts it to a Game_Object object 
		'''
		session = self.make_session()
		game = session.query(Game).filter(id = id).first()
		game_object = Game(1,2)
		game_object.game_id = game.id
		game_object.white = game.white_id
		game_object.black = game.black_id
		game_object.board = game.board
		game_object.game_start = game.start_time
		game_object.n_moves = game.n_moves
		game_object.completed = game.completed 

		game_object.self_board = self.get_moves(game.id)

		for move in game_object.self_board:
			time = move.start_time -move.end_time
			if(move.white == True):
				move.w_clock -= time
				if(move.w_clock < 0):
					game.w_clock = 0
			else:
				move.b_clock -= time
				if(move.b_clock < 0):
					game.b_clock = 0

		return game

	def update_game(self,game,id):
		session = self.make_session()
		get_game = session.query(Game).filter(id = id).first()
		get_game.white_id = game.white
		get_game.black_id = game.black
		get_game.board = game.board
		get_game.n_moves = game.n_moves
		get_game.white = game.white_turn
		get_game.start_time = game.start_time
		get_game.completed = game.start_time
		session.commit()

	def add_move(self,move_object):
		session = self.make_session()
		move = Move(
			move = move_object.move,
			start_time = move_object.start_time,
			end_time = move_object.end_time,
			white = move_object.white,
			move_n = move_object.move_n,
			game_id = move_object.game_id
		)
		session.add(move)
		session.commit()


	def get_moves(self,game_id):
		'''
		Gets all the moves with that game id,
		converts them to move obejcts sorts the list and returns it
		'''
		session = self.make_session()
		all_moves = session.query(Move).filter(game_id = game_id).all()
		for move in all_moves:
			move = Move_Object( 
				white = move.white, 
				move = move.move, 
				move_n = move.move_n, 
				start_time = move.start_time,
				end_time = move.end_time,
				game_id = game_id)
		all_moves.sort(key = lambda x: x.move_n)
		for i in range(0,all_moves):
			if((i == len(all_moves)-1) and all_moves[i].white == False and i%2 == 0):
					temp = all_moves[i+1]
					all_moves[i+1] = all_moves[i]
					all_moves[i] = temp
		return all_moves

	def add_queue(self,que_item):
		session = self.make_session()
		item = Queue(
			time_format = que_item.time_format,
			cpu = que_item.cpu,
			join = que_item.join,
			rating = que_item.rating,
			use_id = que_item.user_id 
			)
		session.add(item)
		session.commit()


	def get_all_queue(self,):
		session = self.make_session()
		queue = session.query(Queue).all()
		changed_queue = []
		for item in queue:
			changed_queue.append(Que_item(item.time_format, item.rating, item.cpu, item.join, item.user_id))
		return changed_queue    	

	def get_queue_item(self,id):
		session = self.make_session()
		queue_item = session.query(Queue).filter(Queue.id == id).first()
		return queue_item	

	def get_queue_item_by_user(self,user_id):
		session = self.make_session()
		queue_item = session.query(Queue).filter(Queue.user_id == user_id).first()
		return queue_item

	def add_user(self,username,email,password):
		session = self.make_session()
		user_object = User(
			username = username,
			email = email,
			password = password)
		session.add(user_object)
		session.commit()

	def remove_player_queue(self,id):
		session = self.make_session()
		post = session.query(Queue).filter(Queue.id == id).delete()
		session.commit()

	def edit_queue(self,id,time_format,cpu,join,rating,user_id,match_id):
		session = self.make_session()
		queue = session.query(Queue).filter(Queue.id == id).first()
		if(time_format != None):
			queue.time_format = time_format
		if(cpu != None):
			queue.cpu = cpu
		if(join != None):
			queue.join = cpu
		if(rating != None):
			queue.user_id = user_id
		if(match_id != None):
			queue.match_id = match_id
		session.commit()

	#Get a specific user from the User table by id and/or username
	def get_user(self,username = None, id = None):
		session = self.make_session()
		if (id == None and username != None):
			user = session.query(User).filter(User.username == username).first()
			return user 
		if(username == None and id != None):
			user = session.query(User).filter(User.id == id).first
			return user
		return None

	def get_user_id(self, id):
		session = self.make_session()
		user = session.query(User).filter(User.id == id).first()
		return user

	def get_game_by_id_not_completed(self, id):
		session = self.make_session()
		game = session.query(Game).filter(or_(Game.black_id == id, Game.white_id == id)).filter(Game.completed == false).first()
		return game