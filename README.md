# Book Reviewer

This program allows you to explore and review books by your favorite authors. You can retrieve book titles, average ratings, and publication dates. Additionally, you can write your own reviews for the books you've read and view reviews made by others and yourself.

## Functions

- `make_google_books_api_request(author_name, num_books)`: Sends a request to the Google Books API and retrieves book information for a specific author. Returns the response data in JSON format.

- `extract_book_titles(data)`: Extracts relevant book titles, average ratings, and publication dates from the retrieved data. Returns a list of tuples representing the book information.

- `save_book_titles_to_database(book_info, books_database)`: Saves the book information to a database. Creates a table named 'book_info_table' in the specified SQLite database and stores the book titles, publication dates, and average ratings.

- `retrieve_from_database(books_database, sort_by)`: Retrieves book information from the database. Returns a DataFrame containing the book titles, publication dates, and average ratings. The results can be sorted by publication date or average rating.

- `write_reviews(retrieve_titles, author_name)`: Allows the user to write a review for a book. Prompts the user to enter the title, rate the book, provide a review, and enter their username. The review is saved in a database table named 'review_table'.

- `display_reviews(aut)`: Displays reviews made by other people for a specific author. Retrieves reviews from the 'review_table' in the database and prints the author name, book title, publication date, rating, review, and username.

## Instructions

1. **Author Search**

   - Enter the name of the author you're interested in.
   - Specify the number of books you would like to display (enter 'all' to access all books).

2. **Retrieve Book Titles**

   - The program will retrieve book titles, average ratings, and publication dates for the specified author.
   - You can choose to sort the retrieved book titles by publication date or average rating.

3. **Write a Review**

   - If you would like to write a review for a book, enter the title of the book.
   - The program will prompt you to rate the book on a scale of 1 to 10 and provide a review.
   - Enter your username for identification.

4. **View Reviews**

   - You can choose to view reviews made by other people for a specific author.
   - Enter the name of the author to see their reviews.

5. **Exit**

   - At any point, you can choose to exit the program.

## Dependencies

This program requires the following dependencies to be installed:

- Python 3
- requests
- pandas
- sqlalchemy

You can install the dependencies by running the following command:
`pip install requests pandas sqlalchemy`

## Usage

1. Make sure you have the required dependencies installed.

2. Run the program.

3. Follow the on-screen prompts to explore and review books by your favorite authors.

Enjoy exploring and reviewing books with the Book Reviewer!


