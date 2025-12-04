import json
from pathlib import Path
from typing import List, Optional
import logging

from .book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.books: List[Book] = []
        self._load()

    def add_book(self, book: Book) -> None:
        if self.search_by_isbn(book.isbn) is not None:
            logger.info(f"Book with ISBN {book.isbn} already exists. Skipping add.")
            return
        self.books.append(book)
        logger.info(f"Book added: {book}")
        self._save()

    def search_by_title(self, title: str) -> List[Book]:
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.error(f"Issue failed: No book with ISBN {isbn}")
            return False
        if not book.issue():
            logger.info(f"Issue failed: Book already issued: {isbn}")
            return False
        logger.info(f"Book issued: {isbn}")
        self._save()
        return True

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.error(f"Return failed: No book with ISBN {isbn}")
            return False
        if not book.return_book():
            logger.info(f"Return failed: Book already available: {isbn}")
            return False
        logger.info(f"Book returned: {isbn}")
        self._save()
        return True

    def _save(self) -> None:
        try:
            data = [b.to_dict() for b in self.books]
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with self.storage_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(self.books)} books to {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to save books: {e}")

    def _load(self) -> None:
        try:
            if not self.storage_path.exists():
                logger.info(f"No storage file found at {self.storage_path}. Starting empty inventory.")
                self.books = []
                return
            with self.storage_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # Validate loaded data is a list of dict-like objects
            self.books = [Book(**item) for item in data]
            logger.info(f"Loaded {len(self.books)} books from {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to load books (file may be missing or corrupted): {e}")
            self.books = []