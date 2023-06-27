import requests 
#import sqlite3 as db 
import pandas as pd
import os
import json
import sqlalchemy as db 


#API integration 
#Make a request to fetch movie data from (---) API

def make_google_books_api_request(subject, num_books):
    url = 'https://www.googleapis.com/books/v1/volumes'
    api_key = os.environ.get('BOOKS_API_KEY')

    query = f'subject:{subject}'


    params = {
        'q': 'subject:{subject}',
        'orderBy': 'rating',
        'maxResults': num_books, 
        'key': api_key
    }

    response = requests.get(url, params = params)
    data = response.json()
    return data


def extract_book_titles(data):
    book_titles = [item['volumeInfo']['title'] for item in data['items']]
    return book_titles

def save_book_titles_to_database(book_titles, database_name):
    data_frame = pd.DataFrame({'book_title': book_titles})
    engine = db.create_engine(f'sqlite:///{database_name}.db')
    data_frame.to_sql('table_name', con=engine, if_exists='replace', index=False)

def retrieve_from_database(database_name):
    engine = db.create_engine(f'sqlite:///{database_name}.db')
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM table_name;")).fetchall()
        return pd.DataFrame(query_result)

subject = input("Enter a subject for a book recomendation: ")
num_books = int(input("Enter the number books to be suggested: "))

data = make_google_books_api_request(subject, num_books)
book_titles = extract_book_titles(data)
save_book_titles_to_database(book_titles, 'database_name')
retrive_titles = retrieve_from_database('database_name')
print(retrive_titles)


# 1. Prompt for subject
# 2. Ask for a genre 
# 3. Ask for prefrences like author 
# 4. ask how many books they want to be suggested 
# 4. Suggest book that match the genre based on high rating
# 5. Ask to choose one book suggesting that they liked very much and use it in future suggestion despite ratings 
