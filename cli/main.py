import sys
import logging
from pathlib import Path

from library_manager.inventory import LibraryInventory
from library_manager.book import Book

# Configure basic logging
LOG_FILE = Path("logs/app.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("library_cli")

STORAGE = Path("data/books.json")

def input_non_empty(prompt: str) -> str:
    while True:
        try:
            value = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled.")
            raise
        if value:
            return value
        print("Input cannot be empty. Please try again.")

def add_book_cli(inv: LibraryInventory):
    try:
        title = input_non_empty("Enter title: ")
        author = input_non_empty("Enter author: ")
        isbn = input_non_empty("Enter ISBN: ")
        book = Book(title=title, author=author, isbn=isbn)
        inv.add_book(book)
        print("Book added.")
    except Exception as e:
        logger.error(f"Error adding book: {e}")

def issue_book_cli(inv: LibraryInventory):
    try:
        isbn = input_non_empty("Enter ISBN to issue: ")
        if inv.issue_book(isbn):
            print("Book issued successfully.")
        else:
            print("Failed to issue book. Check logs or ISBN.")
    except Exception as e:
        logger.error(f"Error issuing book: {e}")

def return_book_cli(inv: LibraryInventory):
    try:
        isbn = input_non_empty("Enter ISBN to return: ")
        if inv.return_book(isbn):
            print("Book returned successfully.")
        else:
            print("Failed to return book. Check logs or ISBN.")
    except Exception as e:
        logger.error(f"Error returning book: {e}")

def view_all_cli(inv: LibraryInventory):
    try:
        all_books = inv.display_all()
        if not all_books:
            print("No books in the inventory.")
            return
        print("\nAll books:")
        for b in all_books:
            print(b)
    except Exception as e:
        logger.error(f"Error displaying books: {e}")

def search_cli(inv: LibraryInventory):
    try:
        choice = input_non_empty("Search by (1) Title or (2) ISBN? Enter 1 or 2: ")
        if choice == "1":
            title = input_non_empty("Enter part or full title: ")
            results = inv.search_by_title(title)
            if not results:
                print("No books found with that title.")
                return
            for b in results:
                print(b)
        elif choice == "2":
            isbn = input_non_empty("Enter ISBN: ")
            book = inv.search_by_isbn(isbn)
            if not book:
                print("No book found with that ISBN.")
                return
            print(book)
        else:
            print("Invalid choice.")
    except Exception as e:
        logger.error(f"Error searching books: {e}")

def main():
    inv = LibraryInventory(STORAGE)

    menu = (
        "\nLibrary Menu:\n"
        "1. Add Book\n"
        "2. Issue Book\n"
        "3. Return Book\n"
        "4. View All Books\n"
        "5. Search Book\n"
        "6. Exit\n"
    )

    while True:
        try:
            print(menu)
            choice = input_non_empty("Enter choice (1-6): ")
            if choice == "1":
                add_book_cli(inv)
            elif choice == "2":
                issue_book_cli(inv)
            elif choice == "3":
                return_book_cli(inv)
            elif choice == "4":
                view_all_cli(inv)
            elif choice == "5":
                search_cli(inv)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Please enter a number between 1 and 6.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")

if __name__ == "__main__":
    main()