import requests
import pandas as pd
import sqlalchemy as db
import os
import json 


def make_google_books_api_request(author_name, num_books):
    url = 'https://www.googleapis.com/books/v1/volumes'
    api_key = os.environ.get('BOOKS_API_KEY')

    params = {
        'q': f'inauthor:{author_name}',  # added 'inauthor' parameter to filter by author
        'orderBy': 'relevance',
        'maxResults': num_books,
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


def extract_book_titles(data):
    book_info = []
    unique_titles = set()
    for item in data['items']:
        title = item['volumeInfo']['title']
        lowercase_title = title.lower()
        published_date = item['volumeInfo'].get('publishedDate', 'Unknown')  # retrieve published date, default to 'Unknown' if not available
        average_rating = item['volumeInfo'].get('averageRating', 0)  # retrieve average rating, default to 0 if not available
        if lowercase_title not in unique_titles:
            unique_titles.add(lowercase_title)
            book_info.append((title, published_date, average_rating))
    
    return book_info


def save_book_titles_to_database(book_info, database_name):
    data_frame = pd.DataFrame(book_info, columns=['book_title', 'published_date', 'average_rating'])
    engine = db.create_engine(f'sqlite:///{database_name}.db')
    with engine.connect() as connection:
        data_frame.to_sql('table_name', con=connection, if_exists='replace', index=False)


def retrieve_from_database(database_name, sort_by):
    engine = db.create_engine(f'sqlite:///{database_name}.db')
    with engine.connect() as connection:
        if sort_by == 'publication':
            query = "SELECT * FROM table_name ORDER BY published_date DESC"  # sort by publication date in descending order
        elif sort_by == 'rating':
            query = "SELECT * FROM table_name ORDER BY average_rating DESC"
        else:
            query = "SELECT * FROM table_name"

        query_result = connection.execute(db.text(query)).fetchall()
        return pd.DataFrame(query_result)

author_name = input("Enter the author name: ")
num_books = input("How many suggestions: ")


data = make_google_books_api_request(author_name, num_books)

if 'items' not in data:
    print("Invalid author name or no books found.")
    exit()


book_info = extract_book_titles(data)
save_book_titles_to_database(book_info, 'database_name')

sort_option = input("Sort by (publication/rating): ")
retrieve_titles = retrieve_from_database('database_name', sort_option)

for index, row in retrieve_titles.iterrows():
    print(f"{index + 1}. {row['book_title']} - {row['published_date']} {row['average_rating']}")
