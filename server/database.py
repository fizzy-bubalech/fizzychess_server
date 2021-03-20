from server.model import Base, Move, Game, User



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


def build_game_move_set(board):
    classname = ticket + "_HistoricDay"
    ticket = type(classname, (Base, HistoricDay), {'__tablename__' : ticket+"_daily_history"})
    ticket.__repr__ =  build_daily_history_table_repr



def add_game(game):
    

