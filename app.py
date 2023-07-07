import git 
from flask import Flask, render_template, url_for, flash, redirect, request
from recomend import make_google_books_api_request, extract_book_titles, save_book_titles_to_database, retrieve_from_database, write_reviews, display_reviews
import requests
import pandas as pd
import sqlalchemy as db
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books', methods=['GET'])
def get_books():
    author_name = request.args.get('author_name')
    num_books = request.args.get('num_books')
    sort_option = request.args.get('sort_option')

    data = make_google_books_api_request(author_name, num_books)
    book_info = extract_book_titles(data)
    save_book_titles_to_database(book_info, 'books_database')

    retrieve_titles = retrieve_from_database('books_database', sort_option)
    book_data = retrieve_titles.to_dict(orient='records')

    return render_template('books.html', book_data=book_data)
from flask import redirect, url_for

@app.route('/write_review', methods=['POST'])
def write_review():
    title = request.form.get('book_title').strip()
    rate = request.form.get('rate')
    review = request.form.get('review')
    username = request.form.get('username')

    review_data = [
        (title, rate, review, username)
    ]

    data_frame = pd.DataFrame(review_data, columns=['title', 'rate', 'review', 'username'])

    reviews_database = "reviews_db"
    engine = db.create_engine(f'sqlite:///{reviews_database}.db')
    with engine.connect() as connection:
        data_frame.to_sql('review_table', con=connection, if_exists='append', index=False)

    print("Review saved successfully!")

    return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/reviews', methods=['GET'])
def reviews():
    title = request.args.get('book_title')

    reviews_database = "reviews_db"
    engine = db.create_engine(f'sqlite:///{reviews_database}.db')
    with engine.connect() as connection:
        query = "SELECT * FROM review_table WHERE title = :title"
        query_result = connection.execute(db.text(query), {"title": title}).fetchall()

        if query_result:
            reviews = []
            for row in query_result:
                book_title = row[1]
                rating = row[3]
                review = row[4]
                reviewed_by = row[5]
                review_info = {
                    'book_title': book_title,
                    'rating': rating,
                    'review': review,
                    'reviewed_by': reviewed_by
                }
                reviews.append(review_info)
            return render_template('reviews.html', reviews=reviews)
        else:
            return render_template('reviews.html', reviews=None)

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/DBandAPI/Google-Book-Reviewer')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
        
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
