
from sqlalchemy import Column, Integer, String, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from sqlalchemy.sql.elements import collate


Base = declarative_base()

class Move(Base):
    __tablename__ = 'moves'
    id = Column(Integer, primary_key = True)
    move = Column(String)
    start_time = Column(Integer)
    end_time = Column(Integer)
    white = Column(Boolean)
    move_n = Column(Integer)
    game_id = Column(Integer)
    
class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key = True)
    white_id = Column(Integer)
    black_id = Column(Integer) 
    board = Column(PickleType) # the board object
    n_moves = Column(Integer) #How many moves was the gae up to the current point
    white = Column(Boolean) #was white the last to play
    start_time = Column(Integer) #in seconds, when white confiremd 
    completed = Column(Boolean) # Has the game been completed
    b_gamestart = Column(Boolean)
    w_gamestart = Column(Boolean)

class User(Base , UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(80))
    rating = Column(Integer)

class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key = True)
    time_format = Column(String(20))
    cpu  = Column(Boolean)
    join = Column(Boolean)
    rating = Column(Integer)
    user_id = Column(String)
    match_id = Column(String)
