import datetime
from sqlalchemy import Column, DateTime, Integer, String, Date, ForeignKey, Float, Boolean, DateTime, PickleType
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


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
    board = Column(PickleType)

class User(Base , UserMixin):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(15), unique=True)
	email = Column(String(50), unique=True)
	password = Column(String(80))

class Queue(Base):
    __tablename__ = 'queue'
    id = Column(Integer, primary_key = True)
    time_format = Column(String(20))
    cpu  = Column(Boolean)
    join = Column(Boolean)
    rating = Column(Integer)
    user_id = Column(String)
    match_id = Column(String)
