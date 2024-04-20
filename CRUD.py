from sqlalchemy import String, Column, Integer, REAL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import database

Base = declarative_base()

engine = create_engine(f'sqlite:///{database.username}.db', echo=False)

connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


class Film_data(Base):
    __tablename__ = 'Film_data'
    Film_id = Column(Integer, primary_key=True)
    Film = Column(String, nullable=False)
    Year = Column(Integer, nullable=False)
    Director = Column(String, nullable=False)
    Stacker_score = Column(REAL, nullable=False)
    Metascore = Column(Integer, nullable=False)
    IMDb_user_rating = Column(REAL, nullable=False)
    Runtime = Column(Integer, nullable=False)


def get_all():
    try:
        with session.begin():
            film_full_list = []
            show_items = int(input('How many films show?: '))
            for film in session.query(Film_data).limit(show_items).all():
                film_full_list.append(f'Film name is {film.Film}, Year {film.Year}  Director is {film.Director} '
                                      f' with Stacker score:{film.Stacker_score}, Metascore: {film.Metascore}'
                                      f' and IMDb rating: {film.IMDb_user_rating} with runtime {film.Runtime}')
        print(f'\n\t{show_items} films are provided.\n')
        return film_full_list
    except Exception as e:
        print("An error occurred:", e)
    finally:

        session.close()



# def del_film():
#
#


