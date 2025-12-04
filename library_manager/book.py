from dataclasses import dataclass, asdict

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"  # 'available' or 'issued'

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self) -> dict:
        return asdict(self)

    def issue(self) -> bool:
        """Mark the book as issued. Return True if success, False if already issued."""
        if self.status == "issued":
            return False
        self.status = "issued"
        return True

    def return_book(self) -> bool:
        """Mark the book as available. Return True if success, False if already available."""
        if self.status == "available":
            return False
        self.status = "available"
        return True

    def is_available(self) -> bool:
        return self.status == "available"