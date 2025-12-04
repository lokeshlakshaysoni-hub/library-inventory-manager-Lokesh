import unittest
from pathlib import Path
import tempfile

from library_manager.inventory import LibraryInventory
from library_manager.book import Book

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.storage = Path(self.tmpdir.name) / "books.json"
        self.inv = LibraryInventory(self.storage)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_and_search(self):
        b = Book(title="A", author="X", isbn="111")
        self.inv.add_book(b)
        found = self.inv.search_by_isbn("111")
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "A")

    def test_issue_and_return(self):
        b = Book(title="B", author="Y", isbn="222")
        self.inv.add_book(b)
        self.assertTrue(self.inv.issue_book("222"))
        self.assertFalse(self.inv.issue_book("222"))  # already issued
        self.assertTrue(self.inv.return_book("222"))
        self.assertFalse(self.inv.return_book("222"))  # already available

    def test_persistence(self):
        b = Book(title="C", author="Z", isbn="333")
        self.inv.add_book(b)
        # create a new inventory pointing to same file
        inv2 = LibraryInventory(self.storage)
        self.assertIsNotNone(inv2.search_by_isbn("333"))

if __name__ == '__main__':
    unittest.main()