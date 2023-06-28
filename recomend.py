import requests
import pandas as pd
import sqlalchemy as db
import os
import json 


def make_google_books_api_request(author_name, num_books):
    url = 'https://www.googleapis.com/books/v1/volumes'
    api_key = os.environ.get('BOOKS_API_KEY')

    # Parameters for the API request, including the author name, sorting order, maximum number of results, and API key
    params = {
        'q': f'inauthor:{author_name}',  # added 'inauthor' parameter to filter by author
        'orderBy': 'relevance',
        'maxResults': num_books,
        'key': api_key
    }
    # Send a GET request to the API endpoint with the specified parameters
    response = requests.get(url, params=params)
    data = response.json()
    # Retrieve the response data in JSON format
    return data

# Function to extract relevant book titles, average rating and published date from the retrieved data
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
    # Convert the title to lowercase for case-insensitive uniqueness check
    return book_info

# Function to save book information to a database
def save_book_titles_to_database(book_info, books_database):

    #It takes book_info (a list containing book information) as input and specifies the column names as
    #'book_title', 'published_date', and 'average_rating'. Each item in book_info is a tuple representing
    # a book's title, published date, and average rating.

    data_frame = pd.DataFrame(book_info, columns=['book_title', 'published_date', 'average_rating'])

    #Create a SQLAlchemy engine for connecting to a SQLite database
    engine = db.create_engine(f'sqlite:///{books_database}.db')

    # Establish a connection to the database
    with engine.connect() as connection:
        # Save the DataFrame as a table named 'book_info_table' in the database to access later in retrieve_from_database
        data_frame.to_sql('book_info_table', con=connection, if_exists='replace', index=False)


def retrieve_from_database(books_database, sort_by):
    engine = db.create_engine(f'sqlite:///{books_database}.db')
    with engine.connect() as connection:
        if sort_by == 'publication':
            #a string to hold the SQL query statement
            query = "SELECT * FROM book_info_table ORDER BY published_date DESC"  # sort by publication date in descending order
        elif sort_by == 'rating':
            query = "SELECT * FROM book_info_table ORDER BY average_rating DESC"
        else:
            #This query retrieves all columns from the table named book_info_table without any specific sorting order.
            query = "SELECT * FROM book_info_table"
        #execute the quert 
        # query_result contains a list of tuples, where each tuple represents a row of the query result.
        query_result = connection.execute(db.text(query)).fetchall()
        #return as a data frame
        return pd.DataFrame(query_result)


def write_reviews(retrieve_titles):
    title = input("Enter the title: ")

    # Check if the title exists in the retrieved titles
    if title in retrieve_titles['book_title'].values:

        selected_book = retrieve_titles.loc[retrieve_titles['book_title'] == title].iloc[0]
        author_name = selected_book['book_title']
        publication_date = selected_book['published_date']

        print(f"Now writing a review for {author_name} - {title} ({publication_date}) - Average Rating: {average_rating}")
        username = input("Enter the username for this review: ")
        rate = int(input ("what would you rate this book on a rate of 1 to 10"))
        review = input("Review: ")

        review_data = [{
            'title': title,
            'author_name': author_name,
            'publication_date': publication_date,
            'review': review,
            'reviewed_by': username,
            'rating': rate
        }]
        data_frame = pd.DataFrame(review_data, columns=['title', 'author_name', 'publication_date', 'review', 'reviewed_by','rating'])
        reviews_database = "reviews_db"
        engine = db.create_engine(f'sqlite:///{reviews_database}.db')
        with engine.connect() as connection:
            if connection.dialect.has_table(connection, 'review_table'):
                data_frame.to_sql('review_table', con=connection, if_exists='append', index=False)
            else:
                data_frame.to_sql('review_table', con=connection, if_exists='replace', index=False)
        print("Review saved successfully!")
        
    else:
        print("Invalid title. Please select a title from the retrieved books.")


def display_reviews():
    reviews_database = "reviews_db"
    engine = db.create_engine(f'sqlite:///{reviews_database}.db')
    with engine.connect() as connection:
        query = "SELECT * FROM review_table"
        query_result = connection.execute(db.text(query)).fetchall()
        review_data = pd.DataFrame(query_result, columns=['title', 'author_name', 'publication_date', 'review', 'reviewed_by', 'rating'])

    # Print the reviews written so far
    print("Reviews in the database:")
    for index, row in review_data.iterrows():
        title = row['title']
        author_name = row['author_name']
        publication_date = row['publication_date']
        review = row['review']
        rating = row['rating']
        reviewed_by = row['reviewed_by']

        print(f"Title: {title}")
        print(f"Author: {author_name}")
        print(f"Publication Date: {publication_date}")
        print(f"Review: {review}")
        print(f"Rating: {rating}")
        print(f"Reviewed By: {reviewed_by}")
        print()

display_reviews()
author_name = input("Enter the author name: ")
num_books = input("How many books would you like displayed: ")

data = make_google_books_api_request(author_name, num_books)

if 'items' not in data:
    print("Invalid author name or no books found.")
    exit()



book_info = extract_book_titles(data)
save_book_titles_to_database(book_info, 'books_database')

sort_option = input("Sort by (publication/rating): ")
retrieve_titles = retrieve_from_database('books_database', sort_option)

for index, row in retrieve_titles.iterrows():
    book_title = row['book_title']
    published_date = row['published_date']
    average_rating = row['average_rating']
    #start indexng from 1 instead of 0
    print(f"{index + 1}. Title: {book_title}")
    print(f"   Published Date: {published_date}")
    print(f"   Average Rating: {average_rating}")
    print()

answer = input("Would you like to write a review to a book? (yes or no): ")

if answer.lower() == 'yes':
    write_reviews(retrieve_titles)
if answer.lower() == 'no':
    display_reviews()
