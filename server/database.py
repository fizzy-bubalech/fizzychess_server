from server.model import Base, Move, Game, User, Queue

from server import Que_item

#imports for the sqlalchemy libary 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Creates the database session
def make_session():
	engine = create_engine('sqlite:///database.db')
	Base.metadata.create_all(engine)
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	return session

def add_game(game):
	session = make_session()
	game = Game(
		game.white,
		game.black,
		game.board)
	session.add(game)
	session.commit()

def add_move(move_object,game_id):
	session = make_session()
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

def add_queue(que_item):
	session = make_session()
	item = Queue(
		time_format = que_item.time_format,
		cpu = que_item.cpu,
		join = que_item.join,
		rating = que_item.rating,
		use_id = que_item.user_id 
		)
	session.add(move)
	session.commit()

def get_all_queue():
	session = make_session()
	queue = session.query(Queue).all()
	changed_queue = []
	for item in queue:
		changed_queue.append(Que_item(item.time_format, item.rating, item.cpu, item.join, item.user_id))
	return changed_queue    	

def get_queue_item(id):
	session = make_session()
	queue_item = session.query(Queue).filter(Queue.id == id).first()
	return queue_item	

def get_queue_item_by_user(user_id):
	session = make_session()
	queue_item = session.query(Queue).filter(Queue.user_id == user_id).first()
	return queue_item

def add_user(username,email,password):
	session = make_session()
	user_object = User(
		username = username,
		email = email,
		password = password)
	session.add(user_object)
	session.commit()

def remove_player_queue(id):
	session = make_session()
	post = session.query(Queue).filter(Queue.id == id).delete()
	session.commit()

def edit_queue(id,time_format,cpu,join,rating,user_id,match_id):
	session = make_session()
	queue = session.query(Queue).filter(Queue.id == id).first()
	if(time_format != None):
		queue.time_format == time_format
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
def get_user(username = None, id = None):
	session = make_session()
	if (id == None and username != None):
		user = session.query(User).filter(User.username == username).first()
		return user 
	if(username == None and id != None):
		user = session.query(User).filter(User.id == id).first
		return user
	return None