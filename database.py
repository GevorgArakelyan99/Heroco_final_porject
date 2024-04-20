import requests
from bs4 import BeautifulSoup
import re
from sqlalchemy import String, Column, Integer, REAL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import sqlite3

try:
    connection = sqlite3.connect("Users.db")
    cursor = connection.cursor()
    cursor.execute('SELECT username FROM User_info ORDER BY ROWID DESC LIMIT 1')
    usernames = cursor.fetchone()
    username = usernames[0]
    connection.close()
except Exception as e:
    username = 'Origin'



def film_DB_adding(log):
    films_data = []

    url = "https://stacker.com/movies/100-best-movies-all-time"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    response.raise_for_status()
    films = soup.find_all('div',
                          class_="paragraph paragraph--type--slideshow-para paragraph--view-mode--full ct-slideshow__slide")

    for film in films:
        film_text = film.h2.get_text()
        cleaned_film_text = re.sub(r'^\W*\d*[\W_]*', '', film_text)
        match = re.search(r'(.+?) \((\d{4})\)', cleaned_film_text)

        film_info = film.p.get_text()
        film_entry = {}

        pattern_to_clean = r"(Directors?|Stacker score|Metascore|IMDb user rating|Runtime): ([^-\n]+)"

        for match_info in re.finditer(pattern_to_clean, film_info):
            label, value = match_info.groups()
            film_entry.update({'name': match.group(1), 'year': match.group(2)})
            if label == "Directors" or label == "Director":
                film_entry['director'] = value.strip()
            elif label == "Stacker score":
                film_entry['stacker_score'] = value.strip()
            elif label == "Metascore":
                film_entry['metascore'] = value.strip()
            elif label == "IMDb user rating":
                film_entry['imdb_rating'] = value.strip()
            elif label == "Runtime":
                film_entry['runtime'] = value.strip()

        films_data.append(film_entry)
    films_data.reverse()

    Base = declarative_base()

    engine = create_engine(f'sqlite:///{username}.db', echo=False)

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

    Base.metadata.create_all(engine)

    for film in films_data:
        data = Film_data(
            Film=film['name'],
            Year=film['year'],
            Director=film['director'],
            Stacker_score=film['stacker_score'],
            Metascore=film['metascore'],
            IMDb_user_rating=film['imdb_rating'],
            Runtime=film['runtime']
        )
        session.add(data)
        session.commit()


