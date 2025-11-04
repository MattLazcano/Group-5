from src import library_functions as lib


class Book:
    """Represents a book in the library catalog."""
    
    def __init__(self, book_id: str, title: str, author: str, genre: str, copies_total: int = 1):
        """Initialize a Book with validation."""
        if not lib.validate_code(book_id):
            raise ValueError(f"Invalid book ID or ISBN: {book_id}")
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if copies_total < 1:
            raise ValueError("Copies must be at least 1.")
        
        self._book_id = book_id
        self._title = title
        self._author = author
        self._genre = genre
        self._copies_total = copies_total
        self._copies_available = copies_total

        book_record = {
        "id": self._book_id,
        "title": self._title,
        "author": self._author,
        "genre": self._genre,
        "tags": set(),
        "copies_total": self._copies_total,
        "copies_available": self._copies_total,
        "waitlist": []
        }

        # Append to shared global catalog
        lib.catalog.append(book_record)
    
    # -------------------------------
    # Properties
    # -------------------------------
    @property
    def book_id(self):
        """str: The unique book ID."""
        return self._book_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def author(self):
        return self._author
    
    @property
    def genre(self):
        return self._genre
    
    @property
    def is_available(self):
        """bool: True if at least one copy is available."""
        return self._copies_available > 0
    
    # -------------------------------
    # Methods (Integrated)
    # -------------------------------
    def check_availability(self) -> bool:
        """Check global catalog to see if book is available."""
        return lib.is_book_available(self._title)

    def add_rating(self, member_id: str, rating: int) -> str:
        """Allow a member to rate this book."""
        return lib.rate_book(member_id, self._book_id, rating)

    def validate_isbn10(self) -> bool:
        """Validate ISBN-10 format."""
        return lib.validate_isbn10_format(self._book_id)

    def validate_isbn13(self) -> bool:
        """Validate ISBN-13 format."""
        return lib.validate_isbn13_format(self._book_id)


    def adjust_copies(self, change: int):
        """Adjust available copies and update global catalog."""
        new_count = self._copies_available + change
        if new_count < 0 or new_count > self._copies_total:
            raise ValueError("Copy count out of range.")

        # Update this instance
        self._copies_available = new_count

        # Also update the global catalog entry if it exists
        for item in lib.catalog:
            if item.get("id") == self._book_id:
                item["copies_available"] = new_count
                break

    
    def __str__(self):
        status = "Available" if self.is_available else "Checked out"
        return f"{self._title} by {self._author} — {status} ({self._copies_available}/{self._copies_total})"
