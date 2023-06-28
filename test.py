import unittest
import sqlite3
import pandas as pd

from book import (
    make_google_books_api_request,
    extract_book_titles,
    save_book_titles_to_database,
    retrieve_from_database,
)


class TestBookAPI(unittest.TestCase):
    def test_api_request(self):
        author_name = "J.K. Rowling"
        num_books = 5
        response = make_google_books_api_request(author_name, num_books)
        self.assertIsNotNone(response)
        self.assertIn('items', response)

    def test_extract_titles(self):
         data = {
             'items': [
                {
                     'volumeInfo': {
                         'title': "Harry Potter and the Philosopher's Stone",
                         'publishedDate': '1997',
                         'averageRating': 4.5
                     }
                 },
                 {
                     'volumeInfo': {
                         'title': 'Harry Potter and the Chamber Secrets',
                         'publishedDate': '1998',
                         'averageRating': 4.6
                     }
                 }
             ]
         }

         book_info = extract_book_titles(data)
         self.assertEqual(len(book_info), 2)
         self.assertEqual(book_info[0][0], "Harry Potter and the Philosopher's Stone")

    def test_save_titles(self):
         book_info = [
             ("Harry Potter and the Philosopher's Stone", '1997', 4.5),
             ('Harry Potter and the Chamber Secrets', '1998', 4.6)
         ]
         books_database = 'test_books'
         save_book_titles_to_database(book_info, books_database)

         # Connect to the database and retrieve the saved data
         connection = sqlite3.connect(f'{books_database}.db')
         cursor = connection.cursor()

         saved_rec = cursor.execute("SELECT * FROM book_info_table").fetchall()

         self.assertEqual(len(saved_rec), len(book_info))

         for i, saved_rec in enumerate(saved_rec):
             exp_title, exp_date, exp_rate = book_info[i]
             self.assertEqual(saved_rec[0], exp_title)
             self.assertEqual(saved_rec[1], exp_date)
             self.assertEqual(saved_rec[2], exp_rate)

         cursor.close()
         connection.close()

    def test_retrieve_from_database(self):
         books_database = 'test_books'
         sort_by = 'publication'
         expected = [
            ("Harry Potter and the Philosopher's Stone", '1997', 4.5)
        ]

         save_book_titles_to_database(expected, books_database)

         result = retrieve_from_database(books_database, sort_by)
         self.assertIsNotNone(result)

        
         self.assertEqual(len(result), len(expected))

         for i in range(len(result)):
             record = result.iloc[i]
             exp_title, exp_date, exp_rating = expected[i]
             self.assertEqual(record['book_title'], exp_title)
             self.assertEqual(record['published_date'], exp_date)
             self.assertEqual(record['average_rating'], exp_rating)


if __name__ == '__main__':
    unittest.main()
