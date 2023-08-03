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
    data_frame = pd.DataFrame(book_info, columns=['book_title', 'published_date', 'average_rating'])

    # Update the engine to use SQLite
    engine = db.create_engine('sqlite:///books_database.db')

    # Establish a connection to the database
    with engine.connect() as connection:
        # Save the DataFrame as a table named 'book_info_table' in the database to access later in retrieve_from_database
        data_frame.to_sql('book_info_table', con=connection, if_exists='replace', index=False)

# Function to retrieve data from the SQLite database
def retrieve_from_database(books_database, sort_by):
    # Update the engine to use SQLite
    engine = db.create_engine('sqlite:///books_database.db')

    with engine.connect() as connection:
        if sort_by == 'publication':
            query = "SELECT * FROM book_info_table ORDER BY published_date DESC"  # sort by publication date in descending order
        elif sort_by == 'rating':
            query = "SELECT * FROM book_info_table ORDER BY average_rating DESC"
        else:
            query = "SELECT * FROM book_info_table"

        query_result = connection.execute(db.text(query)).fetchall()
        return pd.DataFrame(query_result)


def write_reviews(retrieve_titles, author_name):
    title = input("Enter the title: ")

    # Check if the title exists in the retrieved titles
    if title in retrieve_titles['book_title'].values:
        publication_date = retrieve_titles.loc[retrieve_titles['book_title'] == title, 'published_date'].values[0]

        print(f"Now writing a review for {author_name} - {title} ({publication_date})")
        print()
        rate = int(input("What would you rate this book on a scale of 1 to 10? "))
        review = input("Review: ")
        username = input("Enter your username: ")
        print()


        review_data = [
            (
                author_name,
                title,
                publication_date,
                rate,
                review,
                username
            )
        ]

        data_frame = pd.DataFrame(review_data, columns=['author_name', 'title', 'publication_date', 'rate', 'review', 'username'])

        reviews_database = "reviews_db"
        engine = db.create_engine(f'sqlite:///{reviews_database}.db')
        with engine.connect() as connection:
            data_frame.to_sql('review_table', con=connection, if_exists='append', index=False)
        print("Review saved successfully!")
        print()


    else:
        print("Invalid title. Please select a title from the retrieved books.")
        
def display_reviews(aut):
    reviews_database = "reviews_db"
    engine = db.create_engine(f'sqlite:///{reviews_database}.db')
    with engine.connect() as connection:
        query = "SELECT * FROM review_table WHERE author_name LIKE :aut ORDER BY rate DESC"
        query_result = connection.execute(db.text(query), {"aut": aut}).fetchall()
        if query_result:
            for index, row in enumerate(query_result):
                author_name = row[0]
                book_title = row[1]
                published_date = row[2]
                rating = row[3]
                review = row[4]
                reviewed_by = row[5]
                print(f"{index + 1}. Title: {book_title}")
                print(f"   Author: {author_name}")
                print(f"   Published Date: {published_date}")
                print(f"   Rating: {rating}")
                print(f"   Review: {review}")
                print(f"   Reviewed by: {reviewed_by}")
                print()
        else:
            print("No reviews available for this author")

# Uncomment the block of code below if you would like to interact in the terminal instead of the web and run this file

#print()
# print("Welcome to the Book Reviewer!")
# print("This program allows you to explore and review books by your favorite authors.")
# print("You'll be able to retrieve book titles, average ratings, and publication dates.")
# print("Additionally, you can write your own reviews for the books you've read and view reviews made by others and yourself.")
# print()

# author_name = input("Please enter the name of the author you're interested in: ")
# num_books = input("How many books would you like displayed (enetr 'all' to access all books): ")


# if num_books == 'all':
#     num_books = 40



# data = make_google_books_api_request(author_name, num_books)

# if 'items' not in data:
#     print("Invalid author name or no books found.")
#     exit()



# book_info = extract_book_titles(data)
# save_book_titles_to_database(book_info, 'books_database')

# sort_option = input("Sort by (publication/rating): ")
# retrieve_titles = retrieve_from_database('books_database', sort_option)

# for index, row in retrieve_titles.iterrows():
#     book_title = row['book_title']
#     published_date = row['published_date']
#     average_rating = row['average_rating']
#     #start indexng from 1 instead of 0
#     print(f"{index + 1}. Title: {book_title}")
#     print(f"   Published Date: {published_date}")
#     print(f"   Average Rating: {average_rating}")
#     print()


# answer = input("Would you like to write a review to a book? (yes or no): ")

# if answer.lower() == 'yes':
#     write_reviews(retrieve_titles, author_name)
# response = input("would you like to see reviews made by other people?(yes or no): ")
# if response == 'yes':
#     print()
#     aut = input("Enter name of an author: ")
#     display_reviews(aut)
