import unittest
import os
import shutil

from app import Library, Book
from db import DB_NAME


class TestLibrarySafe(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Testler başlamadan ÖNCE çalışır (1 kez).
        Veritabanını yedekler.
        """
        cls.backup_db = "library_backup.db"

        if os.path.exists(DB_NAME):
            shutil.copy(DB_NAME, cls.backup_db)

    @classmethod
    def tearDownClass(cls):
        """
        Testler bittikten SONRA çalışır (1 kez).
        Orijinal veritabanını geri yükler.
        """
        if os.path.exists(cls.backup_db):
            shutil.copy(cls.backup_db, DB_NAME)
            os.remove(cls.backup_db)

    def setUp(self):
        self.library = Library()

    # -------------------------
    # TESTLER
    # -------------------------
    def test_add_book(self):
        book = Book("TEST_KITAP", "TEST_YAZAR", 2025)
        self.library.add_book(book)

        results = self.library.search_by_name("TEST_KITAP")
        self.assertTrue(len(results) >= 1)

    def test_search_book(self):
        results = self.library.search_by_author("TEST_YAZAR")
        self.assertIsInstance(results, list)

    def test_list_books(self):
        books = self.library.list_books()
        self.assertIsInstance(books, list)


if __name__ == "__main__":
    unittest.main()
