import requests 
import sqlite3 as db 
import pandas as pd


#API integration 
#Make a request to fetch movie data from (---) API

def fetch_movie_data():
    api_key = '  '
    url = "       " 
    response = requests.get(url)
    data = response.json()
    return data

#store movie data in the database
def store_movies_in_database(movies):
    engine = db.create_engine('sqlite:///move_recomendation.db')
    con = engine.connect()

    #Defind the table structure 

    table = db.Table(
        'movies',
        db.column('title', db.String),
        db.column('genere', db.String),
        db.column('rating', db.Float), 
    )

    #create the table if it does not exsist
    table.create(engine, checkfirst=True)

    #insert movi data into the table

    for movie in movies:
        query = table.insert().values(title = movie['title'],
        genere = movie['genere'], 
        rating = movie['rating'])

        #somehow execute the quert 
    #close connection 


    #retrieve recomended movies from the data base 

    def get_recomended_movies(fav_mov):
        engine = db.create_engine('sqlite://movie_recomendation.db')
        con = engine.connect()

        #Build the query to retrieve recomended moves where movies matches favorite movie's genere 

        #execute the query and fetch the result 

        return result 


    def main():

        #fetch movie data from API
        movie_data = fetch_movie_data

        #store movie data in the database
        store_movies_in_database(movie_data)

        #user input 
        favoriate_movie = 'title' = input ("Enter your favoriate movie: ")

        #Get recomended movies based on user's favoriate movie

        recomended_movies = get_recomended_movies(favoriate_movie)

        #Display recomeded movies

        print("recomende movies: ")
        for movies in recomend_movies:
            print(movie.title, movie.genere, movie.rating)
    if __name__ == '__main__':
        main()