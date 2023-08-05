# Google Book Lookup

Google Book Lookup is a Flask web application that allows users to explore and review books by their favorite authors. The application utilizes the Google Books API to retrieve book information and provides functionalities to store and display user reviews.

## Features

1. **Home Page**: The home page provides a simple interface to start exploring books.

2. **Get Books**: Users can search for books by entering the author's name, the number of books to display, and the sorting option (publication date or average rating). The application retrieves book information from the Google Books API and saves it to a SQLite database.

3. **Write Reviews**: Users can write reviews for books they have read. They can rate the book on a scale of 1 to 10 and provide a detailed review. The reviews are stored in a separate SQLite database.

4. **Confirmation Page**: After writing a review, users are redirected to a confirmation page, confirming the successful saving of the review.

5. **View Reviews**: Users can view reviews made by other people for a specific book. The reviews are retrieved from the SQLite database and displayed on a separate page.

## Requirements

Before running the application, ensure you have the following dependencies installed:

- Flask
- pandas
- SQLAlchemy
- requests

You can install the required dependencies using pip:

```bash
pip install Flask pandas SQLAlchemy requests
```

## How to Run the Application

1. Clone the repository to your local machine:

```bash
git clone https://github.com/Biruk8/Google-Book-Reviewer.git
cd Google-Book-Reviewer
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

3. Activate the virtual environment:

- Windows:

```bash
venv\Scripts\activate
```

- macOS/Linux:

```bash
source venv/bin/activate
```

4. Run the application:

```bash
python app.py
```

The application should now be running at `http://localhost:5000/` in your web browser.

## Testing

The application includes unit tests for the `recomend.py` module. To run the tests, execute the following command:

```bash
python -m unittest test.py
```

The test suite will execute, and the results will be displayed in the terminal.


Sure, here's the updated section in the README mentioning the option to interact solely on the terminal:

## Terminal Interaction (Optional):


If you prefer to interact solely on the terminal instead of the web interface, you can uncomment the last block of code in `recomend.py` and run `recomend.py` directly. This will provide you with access to all the functionalities through the terminal.

To interact on the terminal, run the following command:

```bash
python recomend.py
```

You can now use the terminal to explore books, write reviews, and view reviews made by others.


## Contributing

Contributions to the Google Book Reviewer project are welcome! If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request.
